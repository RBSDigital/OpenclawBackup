#!/usr/bin/env python3
from __future__ import annotations

import csv
import io
import json
import os
import re
import sys
import subprocess
from dataclasses import dataclass, asdict
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qs, quote_plus, unquote, urljoin, urlparse

import requests
from PIL import Image, ImageOps


OUT_DIR = Path("artifacts/application-logo-pack")
OUT_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    )
}


@dataclass
class AppSpec:
    name: str
    slug: str
    search_query: str
    candidates: list[str]


@dataclass
class ResultRow:
    name: str
    slug: str
    source_page: str
    logo_url: str
    output_file: str
    status: str
    note: str = ""


APPS: list[AppSpec] = [
    AppSpec("Google Analytics", "google_analytics", "Google Analytics official site", ["https://analytics.google.com/"]),
    AppSpec("Adobe Analytics", "adobe_analytics", "Adobe Analytics official site", ["https://business.adobe.com/products/analytics/adobe-analytics.html", "https://www.adobe.com/analytics.html"]),
    AppSpec("OneTrust", "onetrust", "OneTrust official site", ["https://www.onetrust.com/"]),
    AppSpec("Contentsquare", "contentsquare", "Contentsquare official site", ["https://contentsquare.com/"]),
    AppSpec("Qualtrics", "qualtrics", "Qualtrics official site", ["https://www.qualtrics.com/"]),
    AppSpec("Algolia", "algolia", "Algolia official site", ["https://www.algolia.com/"]),
    AppSpec("Adobe Experience Manager", "adobe_experience_manager", "Adobe Experience Manager official site", ["https://business.adobe.com/products/experience-manager/adobe-experience-manager.html"]),
    AppSpec("Adobe Digital Asset Management", "adobe_dam", "Adobe Digital Asset Management official site", ["https://business.adobe.com/products/experience-manager/digital-asset-management.html"]),
    AppSpec("Hootsuite", "hootsuite", "Hootsuite official site", ["https://www.hootsuite.com/"]),
    AppSpec("Talkwalker", "talkwalker", "Talkwalker official site", ["https://www.talkwalker.com/"]),
    AppSpec("Magento", "magento", "Magento official site", ["https://business.adobe.com/products/magento/open-source.html", "https://business.adobe.com/products/magento/adobe-commerce.html"]),
    AppSpec("Shopify", "shopify", "Shopify official site", ["https://www.shopify.com/"]),
    AppSpec("WorldPay", "worldpay", "Worldpay official site", ["https://www.worldpay.com/"]),
    AppSpec("Recharge", "recharge", "Recharge official site", ["https://rechargepayments.com/"]),
    AppSpec("Amasty", "amasty", "Amasty official site", ["https://amasty.com/"]),
    AppSpec("Yotpo", "yotpo", "Yotpo official site", ["https://www.yotpo.com/"]),
    AppSpec("Yoti", "yoti", "Yoti official site", ["https://www.yoti.com/"]),
    AppSpec("Mapbox", "mapbox", "Mapbox official site", ["https://www.mapbox.com/"]),
    AppSpec("Open Loyalty", "open_loyalty", "Open Loyalty official site", ["https://www.openloyalty.io/"]),
    AppSpec("UCC", "ucc", "UCC 1-2-1 Agency official site", []),
    AppSpec("myGlo", "myglo", "myGlo official site", ["https://www.myglo.com/"]),
    AppSpec("myVuse", "myvuse", "myVuse official site", ["https://www.vuse.com/", "https://www.vuse.com/ca/en", "https://myvuse.com/"]),
    AppSpec("Azure Integration Services", "azure_integration_services", "Azure Integration Services official site", ["https://azure.microsoft.com/en-us/products/integration-services/"]),
    AppSpec("Salesforce Service Cloud", "salesforce_service_cloud", "Salesforce Service Cloud official site", ["https://www.salesforce.com/products/service-cloud/overview/"]),
    AppSpec("Salesforce Sales Cloud", "salesforce_sales_cloud", "Salesforce Sales Cloud official site", ["https://www.salesforce.com/products/sales-cloud/overview/"]),
    AppSpec("Salesforce Marketing Cloud", "salesforce_marketing_cloud", "Salesforce Marketing Cloud official site", ["https://www.salesforce.com/products/marketing-cloud/overview/"]),
    AppSpec("Salesforce Community Cloud", "salesforce_community_cloud", "Salesforce Community Cloud official site", ["https://www.salesforce.com/products/community-cloud/overview/", "https://www.salesforce.com/products/experience-cloud/overview/"]),
    AppSpec("HubSpot CRM", "hubspot_crm", "HubSpot CRM official site", ["https://www.hubspot.com/products/crm"]),
    AppSpec("BulkSMS", "bulksms", "BulkSMS official site", ["https://www.bulksms.com/"]),
    AppSpec("Vodafone", "vodafone", "Vodafone official site", ["https://www.vodafone.com/"]),
    AppSpec("Heroku Platform", "heroku_platform", "Heroku official site", ["https://www.heroku.com/"]),
    AppSpec("Azure Data Factory", "azure_data_factory", "Azure Data Factory official site", ["https://azure.microsoft.com/en-us/products/data-factory/"]),
    AppSpec("Microsoft Fabric", "microsoft_fabric", "Microsoft Fabric official site", ["https://www.microsoft.com/en-us/microsoft-fabric", "https://fabric.microsoft.com/"]),
    AppSpec("EDP", "edp", "Enterprise Data Platform official site", []),
]


class IconParser(HTMLParser):
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.link_candidates: list[str] = []
        self.image_candidates: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        attrs_d = {k.lower(): (v or "") for k, v in attrs}
        if tag.lower() == "link":
            rel = attrs_d.get("rel", "").lower()
            href = attrs_d.get("href", "").strip()
            if not href:
                return
            if any(key in rel for key in ("icon", "shortcut", "apple-touch-icon", "mask-icon")):
                self.link_candidates.append(urljoin(self.base_url, href))
        elif tag.lower() == "meta":
            key = [REDACTED_SECRET]"property", "") + " " + attrs_d.get("name", "")).lower()
            content = attrs_d.get("content", "").strip()
            if content and any(key_name in key for key_name in ("og:image", "twitter:image", "twitter:image:src")):
                self.image_candidates.append(urljoin(self.base_url, content))
        elif tag.lower() == "img":
            src = attrs_d.get("src", "").strip() or attrs_d.get("data-src", "").strip()
            if not src:
                return
            hint = " ".join(
                [attrs_d.get("alt", ""), attrs_d.get("title", ""), attrs_d.get("class", ""), attrs_d.get("id", ""), attrs_d.get("aria-label", "")]
            ).lower()
            if any(word in hint for word in ("logo", "brand", "mark", "icon", "wordmark")):
                self.image_candidates.append(urljoin(self.base_url, src))


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def fetch_text(url: str, timeout: int = 3) -> tuple[str, str]:
    resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
    resp.raise_for_status()
    return resp.text, resp.url


def fetch_bytes(url: str, timeout: int = 3) -> tuple[bytes, str, str]:
    resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
    resp.raise_for_status()
    content_type = resp.headers.get("content-type", "").split(";")[0].strip().lower()
    return resp.content, content_type, resp.url


def ddg_search(query: str) -> list[str]:
    search_url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    html, _ = fetch_text(search_url, timeout=25)
    links = []
    for href in re.findall(r'href="(.*?)"', html):
        if "uddg=" in href:
            parsed = urlparse(href)
            qs = parse_qs(parsed.query)
            target = qs.get("uddg", [""])[0]
            if target:
                links.append(unquote(target))
    if links:
        return links
    for m in re.finditer(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"', html):
        href = m.group(1)
        if "uddg=" in href:
            parsed = urlparse(href)
            qs = parse_qs(parsed.query)
            target = qs.get("uddg", [""])[0]
            if target:
                links.append(unquote(target))
    return links


def score_candidate(url: str) -> int:
    lower = url.lower()
    score = 0
    if any(ext in lower for ext in (".png", ".ico", ".svg", ".webp")):
        score += 10
    if "logo" in lower:
        score += 8
    if "brand" in lower or "wordmark" in lower:
        score += 6
    if "icon" in lower or "favicon" in lower:
        score += 4
    if "apple-touch-icon" in lower:
        score += 3
    if "og:image" in lower:
        score += 1
    return score


def choose_logo_url(page_url: str, html: str) -> str | None:
    parser = IconParser(page_url)
    parser.feed(html)
    candidates = parser.link_candidates + parser.image_candidates
    if not candidates:
        parsed = urlparse(page_url)
        root = f"{parsed.scheme}://{parsed.netloc}"
        candidates = [
            urljoin(root, "/favicon.ico"),
            urljoin(root, "/favicon.png"),
            urljoin(root, "/apple-touch-icon.png"),
            urljoin(root, "/apple-touch-icon-precomposed.png"),
        ]
    ranked = sorted(dict.fromkeys(candidates), key=[REDACTED_SECRET], reverse=True)
    return ranked[0] if ranked else None


def looks_like_svg(url: str, content_type: str, payload: bytes) -> bool:
    if "svg" in content_type:
        return True
    lower = url.lower()
    if lower.endswith(".svg") or lower.endswith(".svgz"):
        return True
    head = payload.lstrip()[:200].lower()
    return head.startswith(b"<?xml") and b"<svg" in head or head.startswith(b"<svg")


def rasterize_svg(payload: bytes) -> bytes:
    node_script = r"""
const sharp = require('sharp');
const chunks = [];
process.stdin.on('data', chunk => chunks.push(chunk));
process.stdin.on('end', async () => {
  try {
    const input = Buffer.concat(chunks);
    const out = await sharp(input, { density: 300 })
      .resize({ width: 48, height: 48, fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
      .png()
      .toBuffer();
    process.stdout.write(out);
  } catch (err) {
    console.error(err && err.stack ? err.stack : String(err));
    process.exit(1);
  }
});
"""
    proc = subprocess.run(
        ["node", "-e", node_script],
        input=payload,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace").strip() or "sharp SVG rasterization failed")
    return proc.stdout


def normalize_image(payload: bytes, content_type: str, url: str, output_path: Path) -> None:
    if looks_like_svg(url, content_type, payload):
        png_bytes = rasterize_svg(payload)
        img = Image.open(io.BytesIO(png_bytes))
    else:
        img = Image.open(io.BytesIO(payload))
    img = img.convert("RGBA")
    img = ImageOps.contain(img, (48, 48), method=Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    canvas.alpha_composite(img, ((48 - img.width) // 2, (48 - img.height) // 2))
    canvas.save(output_path, format="PNG", optimize=True)


def resolve_source(app: AppSpec) -> str | None:
    for candidate in app.candidates:
        return candidate

    search_results = ddg_search(app.search_query)
    for result in search_results:
        if any(bad in result.lower() for bad in ("wikipedia.org", "facebook.com", "linkedin.com", "play.google.com", "apps.apple.com", "softonic.com", "law.cornell.edu", "uniformlaws.org")):
            continue
        return result
    return None


def favicon_candidates(source_url: str) -> list[str]:
    parsed = urlparse(source_url)
    root = f"{parsed.scheme}://{parsed.netloc}"
    return [
        urljoin(root, "/favicon.ico"),
        urljoin(root, "/favicon.png"),
        urljoin(root, "/apple-touch-icon.png"),
        urljoin(root, "/apple-touch-icon-precomposed.png"),
    ]


def extract_logo(source_url: str) -> tuple[bytes, str, str]:
    last_error: Exception | None = None
    for candidate in favicon_candidates(source_url):
        try:
            payload, content_type, final_url = fetch_bytes(candidate)
            if payload:
                return payload, content_type, final_url
        except Exception as exc:
            last_error = exc

    html = ""
    try:
        html, final_page = fetch_text(source_url)
        logo_url = choose_logo_url(final_page, html)
        if logo_url:
            payload, content_type, final_url = fetch_bytes(logo_url)
            return payload, content_type, final_url
    except Exception as exc:
        last_error = exc

    if last_error:
        raise last_error
    raise RuntimeError(f"Unable to extract a logo from {source_url}")


def main() -> int:
    rows: list[ResultRow] = []
    for app in APPS:
        source_page = resolve_source(app)
        if not source_page:
            rows.append(ResultRow(app.name, app.slug, "", "", "", "unresolved", "No reachable official page found"))
            continue

        try:
            payload, content_type, final_url = extract_logo(source_page)
            out_file = OUT_DIR / f"{app.slug}.png"
            normalize_image(payload, content_type, final_url, out_file)
            rows.append(ResultRow(app.name, app.slug, source_page, final_url, str(out_file), "ok"))
            print(f"[ok] {app.name}: {final_url} -> {out_file}")
        except Exception as exc:
            rows.append(ResultRow(app.name, app.slug, source_page, "", "", "failed", f"{type(exc).__name__}: {exc}"))
            print(f"[fail] {app.name}: {source_page} -> {exc}", file=sys.stderr)

    manifest_json = OUT_DIR / "manifest.json"
    manifest_csv = OUT_DIR / "manifest.csv"
    with manifest_json.open("w", encoding="utf-8") as f:
        json.dump([asdict(row) for row in rows], f, indent=2)
    with manifest_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()) if rows else list(ResultRow("", "", "", "", "", "").__dict__.keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))

    ok_count = sum(1 for row in rows if row.status == "ok")
    print(f"Completed {ok_count}/{len(rows)} logo extractions into {OUT_DIR}")
    return 0 if ok_count else 1


if __name__ == "__main__":
    raise SystemExit(main())
