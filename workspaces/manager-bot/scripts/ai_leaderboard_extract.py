#!/usr/bin/env python3
"""Fetch and normalize the requested LiveBench and Scale leaderboard data.

This is deliberately dependency-free.  The sites are presentation-oriented and
occasionally block generic clients, so requests use a browser-like identity,
retry transient responses, and validate that ranking rows were actually found.
"""
from __future__ import annotations

import argparse
import csv
import html
import io
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131 Safari/537.36"
LIVEBENCH = "https://livebench.ai"
SCALE = "https://labs.scale.com/leaderboard"
SCALE_SLUGS = {
    "SciPredict": "scipredict",
    "Humanity's Last Exam": "humanitys_last_exam",
    "Professional Reasoning: Finance": "prbench-finance",
    "Professional Reasoning: Legal": "prbench-legal",
}


class FetchFailure(RuntimeError):
    pass


def fetch(url: str, attempts: int = 2, deadline: float | None = None) -> tuple[int, str]:
    last = None
    for n in range(attempts):
        remaining = 12.0 if deadline is None else max(0.1, deadline - time.monotonic())
        if deadline is not None and remaining <= 0:
            break
        try:
            req = Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/json,text/csv,*/*"})
            with urlopen(req, timeout=min(12.0, remaining)) as response:
                return response.status, response.read().decode("utf-8", "replace")
        except HTTPError as exc:
            if exc.code == 404:
                raise FetchFailure(f"404 Not Found: {url}") from exc
            last = exc
            if n + 1 < attempts and (deadline is None or time.monotonic() < deadline):
                time.sleep(min(1 + n, max(0.1, deadline - time.monotonic()) if deadline else 1 + n))
        except (URLError, TimeoutError) as exc:
            last = exc
            if n + 1 < attempts and (deadline is None or time.monotonic() < deadline):
                time.sleep(min(1 + n, max(0.1, deadline - time.monotonic()) if deadline else 1 + n))
    raise FetchFailure(f"fetch failed after {attempts} attempts: {url}: {last}")


def numbers(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def livebench_metadata(js: str, model: str) -> dict:
    """Read metadata from the compiled bundle without executing untrusted JS."""
    pos = js.find(model)
    if pos < 0:
        return {"model": model, "display_name": model, "provider": None, "open_weights": None}
    # A model object normally ends before the next top-level quoted key. A
    # bounded window is safer than trying to evaluate the site's JS bundle.
    end_match = re.search(r'},"[A-Za-z0-9_.-]+":\{', js[pos + len(model):])
    window = js[pos : pos + len(model) + (end_match.start() if end_match else 2400)]
    display = re.search(r'displayName:"([^"]+)"', window)
    org = re.search(r'organization:"([^"]+)"', window)
    return {
        "model": model,
        "display_name": display.group(1) if display else model,
        "provider": org.group(1) if org else None,
        "open_weights": bool(re.search(r'openweight:!0', window)),
    }


def _weighted_average(scores: dict, categories: dict, weights: dict | None = None) -> float:
    weights = weights or {}
    parts = []
    for name, cols in categories.items():
        vals = [scores.get(c) for c in cols if scores.get(c) is not None]
        if vals:
            parts.append((sum(vals) / len(vals), float(weights.get(name, 1.0))))
    if not parts:
        return 0.0
    return sum(value * weight for value, weight in parts) / sum(weight for _, weight in parts)


def _build_livebench_result(release: str, table_text: str, categories_text: str,
                            cost_text: str | None, js: str, url: str, gen: str) -> dict:
    table = list(csv.DictReader(io.StringIO(table_text)))
    categories_raw = json.loads(categories_text)
    weights = categories_raw.pop("_overall_weights", {}) if isinstance(categories_raw, dict) else {}
    categories = categories_raw
    costs = {r.get("model"): r for r in csv.DictReader(io.StringIO(cost_text or ""))} if cost_text else {}
    if len(table) < 2 or not categories:
        raise RuntimeError("assets contained no usable rows or categories")
    task_columns = [k for k in table[0] if k != "model"]
    models = []
    for row in table:
        if not row.get("model"):
            continue
        meta = livebench_metadata(js, row["model"])
        scores = {k: numbers(row.get(k)) for k in task_columns}
        category_scores = {}
        for name, cols in categories.items():
            vals = [scores.get(c) for c in cols if scores.get(c) is not None]
            if vals:
                category_scores[name] = round(sum(vals) / len(vals), 3)
        direct_cost = costs.get(row["model"], {}).get("cost_per_successful_task")
        models.append({**meta, "overall": round(_weighted_average(scores, categories, weights), 3),
                       "categories": category_scores,
                       "cost_per_successful_task": numbers(direct_cost)})
    if not models:
        raise RuntimeError("table contained no model rows")
    def top(key):
        return sorted(models, key=[REDACTED_SECRET] x: x.get(key) if isinstance(x.get(key), (int, float)) else -1, reverse=True)[:10]
    return {"source": "LiveBench", "release": release, "generation": gen, "url": url,
            "models": len(models), "overall_leaders": top("overall"),
            "open_weight_leaders": sorted([x for x in models if x["open_weights"]], key=[REDACTED_SECRET] x: x["overall"], reverse=True)[:10],
            "categories": {name: sorted(models, key=[REDACTED_SECRET] x: x["categories"].get(name, -1), reverse=True)[:10] for name in categories},
            "cost_leaders": sorted([x for x in models if x["cost_per_successful_task"] and x["cost_per_successful_task"] > 0], key=[REDACTED_SECRET] x: x["cost_per_successful_task"])[:10]}


def livebench(deadline: float) -> dict:
    _, home = fetch(LIVEBENCH + "/", deadline=deadline)
    scripts = re.findall(r'(?:src|href)=["\']([^"\']+\.js)["\']', home)
    js = ""
    for path in scripts:
        if not path.startswith("http"):
            path = LIVEBENCH + "/" + path.lstrip("/")
        try:
            _, js = fetch(path, deadline=deadline)
            if "table_" in js or "openweight" in js:
                break
        except RuntimeError:
            continue
    separated = re.findall(r"(\d{4})[_-](\d{2})[_-](\d{2})", home + js)
    compact = re.findall(r"(?<!\d)(\d{4})(\d{2})(\d{2})(?!\d)", home + js)
    releases = sorted(set(separated + compact), reverse=True)
    if not releases:
        raise RuntimeError("LiveBench release list was not found")
    last_error = None
    for y, m, d in releases[:8]:
        release = f"{y}-{m}-{d}"
        suffix = f"{y}_{m}_{d}"
        try:
            if y + m + d >= "20261014":
                base = f"{LIVEBENCH}/data/{y}{m}{d}"
                _, table_text = fetch(f"{base}/table.csv?v=1793398874", deadline=deadline)
                _, categories_text = fetch(f"{base}/categories.json?v=1793398874", deadline=deadline)
                try:
                    _, cost_text = fetch(f"{base}/cost.csv?v=1793398874", deadline=deadline)
                except FetchFailure:
                    cost_text = None
                return _build_livebench_result(release, table_text, categories_text, cost_text, js, LIVEBENCH + "/#", "v2")
            _, table_text = fetch(f"{LIVEBENCH}/v1/table_{suffix}.csv?v=1793398874", deadline=deadline)
            _, categories_text = fetch(f"{LIVEBENCH}/v1/categories_{suffix}.json?v=1793398874", deadline=deadline)
            try:
                _, cost_text = fetch(f"{LIVEBENCH}/v1/cost_{suffix}.csv?v=1793398874", deadline=deadline)
            except FetchFailure:
                cost_text = None
            return _build_livebench_result(release, table_text, categories_text, cost_text, js, LIVEBENCH + "/#", "v1")
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"LiveBench assets could not be parsed: {last_error}")


def scale_page(name: str, slug: str, deadline: float) -> dict:
    _, page = fetch(f"{SCALE}/{slug}", deadline=deadline)
    start = page.find("Performance Comparison")
    if start < 0:
        raise RuntimeError(f"{name}: Performance Comparison section not found")
    sub = page[start:]
    rows = []
    for match in re.finditer(r'data-model-name="true"[^>]*>(.*?)</p>', sub):
        before = sub[max(0, match.start() - 3000):match.start()]
        after = sub[match.end():match.end() + 2200]
        ranks = re.findall(r'rounded-full text-xs font-mono font-medium[^>]*>(\d+)</span>', before)
        scores = re.findall(r'<span class="text-ink">([^<]+)</span>', after)
        if not ranks or not scores:
            continue
        ci = re.findall(r'text-neutral-600">[^<]*<!-- -->([^<]+)', after)
        calib = re.search(r'Calib Err:.*?<!-- -->\s*<!-- -->([^<]+)', after)
        rows.append({"rank": int(ranks[-1]), "model": html.unescape(re.sub(r"\s+", " ", match.group(1))).strip(),
                     "score": numbers(scores[0]), "uncertainty": numbers(ci[0]) if ci else None,
                     "calibration_error": numbers(calib.group(1)) if calib else None})
    # Preserve displayed ranks and de-duplicate rows created by nested markup.
    unique = []
    seen = set()
    for row in rows:
        key = [REDACTED_SECRET]"rank"], row["model"], row["score"])
        if key not in seen:
            seen.add(key); unique.append(row)
    if not unique:
        raise RuntimeError(f"{name}: no ranking rows found")
    return {"benchmark": name, "slug": slug, "url": f"{SCALE}/{slug}", "rows": unique}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="write JSON to this path")
    parser.add_argument("--timeout-seconds", type=float, default=240)
    args = parser.parse_args()
    deadline = time.monotonic() + args.timeout_seconds
    result = {"extracted_at": datetime.now(timezone.utc).isoformat(), "livebench": None, "scale": []}
    result["livebench"] = livebench(deadline)
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(scale_page, name, slug, deadline): name for name, slug in SCALE_SLUGS.items()}
        for future in as_completed(futures):
            result["scale"].append(future.result())
    result["scale"].sort(key=[REDACTED_SECRET] x: x["benchmark"])
    if len(result["livebench"]["overall_leaders"]) < 1 or any(len(x["rows"]) < 1 for x in result["scale"]):
        raise RuntimeError("validation failed: one or more sources returned no usable rankings")
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
