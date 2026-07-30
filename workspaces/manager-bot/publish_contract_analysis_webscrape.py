#!/usr/bin/env python3
"""Publish the daily JobServe contract analysis sheet to Google Drive.

This script takes the local sheet payloads produced by the scrape flow,
creates or reuses the dated spreadsheet in the
`Contract_Analysis_WebScrape` Drive folder, and writes the Results and
Summary tabs.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FOLDER_ID = "1QrEU8Ckhbs7Bk1E0FE7G0m3NFpdoj4Wd"
TEMPLATE_SPREADSHEET_ID = "1k8fBgFxTGPfJSK7T5sbWLtCuRJcpcpw-q4PfWi4p064"
RESULTS_PATH = Path("sheet_values.json")
SUMMARY_PATH = Path("summary_values.json")
TITLE_PREFIX = "Contract_Analysis_WebScrape_"


def run_gog(args: list[str]) -> dict[str, Any]:
    cmd = ["gog", "--json", *args]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"gog {' '.join(args)} failed with exit code {proc.returncode}\n"
            f"stdout:\n{proc.stdout}\n"
            f"stderr:\n{proc.stderr}"
        )
    output = proc.stdout.strip()
    if not output:
        return {}
    try:
        return json.loads(output)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"gog {' '.join(args)} returned non-JSON output:\n{output}") from exc


def load_matrix(path: Path) -> list[list[Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required payload file: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or any(not isinstance(row, list) for row in data):
        raise ValueError(f"{path} does not contain a 2D JSON array")
    return data


def find_existing_sheet(title: str) -> str | None:
    result = run_gog(["drive", "search", title])
    for file in result.get("files", []):
        if file.get("mimeType") != "application/vnd.google-apps.spreadsheet":
            continue
        if file.get("name") != title:
            continue
        parents = file.get("parents") or []
        if FOLDER_ID in parents:
            return file["id"]
    return None


def copy_template(title: str) -> str:
    result = run_gog(["sheets", "copy", TEMPLATE_SPREADSHEET_ID, title, "--parent", FOLDER_ID])
    spreadsheet_id = result.get("spreadsheetId") or (result.get("file") or {}).get("id")
    if not spreadsheet_id:
        raise RuntimeError(f"Could not determine spreadsheetId from copy result: {result}")
    return spreadsheet_id


def clear_range(spreadsheet_id: str, sheet_range: str) -> None:
    run_gog(["sheets", "clear", spreadsheet_id, sheet_range])


def update_range(spreadsheet_id: str, sheet_range: str, values: list[list[Any]]) -> None:
    run_gog(
        [
            "sheets",
            "update",
            spreadsheet_id,
            sheet_range,
            "--values-json",
            json.dumps(values, ensure_ascii=False),
        ]
    )


def main() -> int:
    title = f"{TITLE_PREFIX}{datetime.now(timezone.utc).date().isoformat()}"
    results = load_matrix(RESULTS_PATH)
    summary = load_matrix(SUMMARY_PATH)

    spreadsheet_id = find_existing_sheet(title)
    if spreadsheet_id is None:
        spreadsheet_id = copy_template(title)

    # Start from a clean slate so reruns don't leave stale rows behind.
    clear_range(spreadsheet_id, "Results!A1:Z1000")
    clear_range(spreadsheet_id, "Summary!A1:Z1000")
    update_range(spreadsheet_id, "Results!A1", results)
    update_range(spreadsheet_id, "Summary!A1", summary)

    web_url = run_gog(["drive", "url", spreadsheet_id])
    print(json.dumps({"spreadsheetId": spreadsheet_id, "title": title, "url": web_url}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
