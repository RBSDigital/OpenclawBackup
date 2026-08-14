#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus

from jobserve_contract_analysis import BASE, TARGETS, detail, fetch, parse_listing, parse_posted_age, title_aliases

OUT_CSV = Path("contract_analysis_jobserve.csv")
OUT_JSON = Path("contract_analysis_jobserve.json")
SHEET_VALUES = Path("sheet_values.json")
SUMMARY_VALUES = Path("summary_values.json")
SOURCE_URL = "https://it.jobserve.com/JobSearch?q=business%20analysis&l=&dist=50"
QUERY_LIST = ["Outside IR35"] + [f"{t} Outside IR35" for t in TARGETS] + TARGETS
MAX_RESULTS_PER_TITLE = 10
MAX_PAGES = 12
TAG_RE = re.compile(r"<[^>]+>")


def clean_html_text(value: str) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", TAG_RE.sub(" ", value)).strip()


def fetch_pool() -> list[dict]:
    pool: list[dict] = []
    seen: set[str] = set()
    for q in QUERY_LIST:
        first = fetch(f"{BASE}/JobSearch?q={quote_plus(q)}&l=&dist=50&jt=c")
        m = re.search(r"Page\s+1\s+of\s+(\d+)", first)
        pages = min(int(m.group(1)) if m else 1, MAX_PAGES)
        for page in range(1, pages + 1):
            html = first if page == 1 else fetch(f"{BASE}/JobSearch?q={quote_plus(q)}&l=&dist=50&jt=c&page={page}")
            for item in parse_listing(html):
                if item["url"] in seen:
                    continue
                try:
                    d = detail(item["url"])
                except Exception:
                    continue

                text_blob = " ".join(
                    [
                        item.get("title", ""),
                        item.get("snippet", ""),
                        item.get("salary_location", ""),
                        d.get("source_title", ""),
                        d.get("description", ""),
                        d.get("posted", ""),
                    ]
                ).lower()
                if "outside ir35" not in text_blob:
                    continue

                if (d.get("job_type") or "").lower() != "contract" and "contractor" not in (d.get("employment_type") or "").lower():
                    continue

                age = parse_posted_age(item.get("posted"))
                if age is None:
                    age = parse_posted_age(d.get("posted"))
                if age is None or age > 5:
                    continue

                seen.add(item["url"])
                pool.append({**item, **d, "age_days": age})
                time.sleep(0.18)
    return pool


def match_score(target: str, row: dict) -> int:
    aliases = title_aliases(target)
    source_title = (row.get("source_title") or row.get("title") or "").lower()
    description = (row.get("description") or "").lower()
    title_blob = f"{source_title} {description}"
    score = 0
    for alias in aliases:
        if alias in source_title:
            score = max(score, 100 - aliases.index(alias))
        if alias in title_blob:
            score = max(score, 80 - aliases.index(alias))
    if target == "Business Analyst":
        if "business analyst" in title_blob:
            score = max(score, 70)
    return score


def best_target(row: dict) -> tuple[str | None, int]:
    best = None
    best_score = 0
    for target in TARGETS:
        score = match_score(target, row)
        if score > best_score:
            best = target
            best_score = score
    return best, best_score


def build_rows(pool: list[dict]) -> tuple[list[list], list[list]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in pool:
        target, score = best_target(row)
        if target is None or score <= 0:
            continue
        row = dict(row)
        row["assigned_target"] = target
        row["match_score"] = score
        grouped[target].append(row)

    results: list[list] = []
    summary: list[list] = [["Requested Job Title", "Matching roles found", "Target roles requested", "Shortfall", "Notes"]]
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    for target in TARGETS:
        rows = grouped.get(target, [])
        rows.sort(key=[REDACTED_SECRET] r: (-r["match_score"], r.get("age_days", 999), r.get("source_title") or r.get("title") or "", r.get("url") or ""))
        rows = rows[:MAX_RESULTS_PER_TITLE]
        for index, row in enumerate(rows, start=1):
            results.append(
                [
                    target,
                    index,
                    row.get("source_title") or row.get("title") or "",
                    row.get("company") or "",
                    row.get("location") or "",
                    row.get("salary") or row.get("salary_location") or "",
                    row.get("job_type") or row.get("employment_type") or "",
                    row.get("posted") or "",
                    "OUTSIDE IR35 found in role description",
                    row.get("url") or "",
                    row.get("description") or "",
                    now,
                ]
            )
        count = len(rows)
        shortfall = MAX_RESULTS_PER_TITLE - count
        if shortfall <= 0:
            note = "Target met"
        else:
            note = f"Only {count} matching Contract roles with OUTSIDE IR35 in the advert and posted within the last 5 days were available on JobServe at retrieval time."
        summary.append([target, count, MAX_RESULTS_PER_TITLE, shortfall, note])

    summary.append([
        "Source",
        SOURCE_URL,
        "",
        "",
        "Filtered to Contract results with OUTSIDE IR35 in advert/snippet and posting age <= 5 days.",
    ])
    return results, summary


def main() -> None:
    pool = fetch_pool()
    results, summary = build_rows(pool)

    fields = [
        "Requested Job Title",
        "Result #",
        "Job Title",
        "Company",
        "Location",
        "Salary",
        "Job Type",
        "Posted",
        "IR35 Filter",
        "JobServe URL",
        "Role Description",
        "Retrieved At UTC",
    ]
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        writer.writerows(results)

    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(
            [
                {field: value for field, value in zip(fields, row)}
                for row in results
            ],
            f,
            ensure_ascii=False,
            indent=2,
        )

    SHEET_VALUES.write_text(json.dumps([fields, *results], ensure_ascii=False, indent=2), encoding="utf-8")
    SUMMARY_VALUES.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    counts = {row[0]: row[1] for row in summary if row and row[0] in TARGETS}
    for target in TARGETS:
        print(f"{target}: {counts.get(target, 0)}")
    print(f"wrote {OUT_CSV} rows={len(results)}")


if __name__ == "__main__":
    main()
