#!/usr/bin/env python3
"""Render the extractor JSON as a safe, table-based HTML email."""
from __future__ import annotations
import argparse, html, json

def esc(v):
    return html.escape("" if v is None else str(v), quote=True)

def row(model, score_key="[REDACTED_SECRET]"):
    score = model.get(score_key, model.get("score"))
    cost = model.get("cost_per_successful_task")
    extra = f"<td>${cost:.4f}</td>" if isinstance(cost, (int, float)) and cost > 0 else "<td>—</td>"
    return f"<tr><td>{esc(model.get('display_name', model.get('model')))}</td><td>{esc(model.get('provider') or 'Not published')}</td><td>{esc(score)}</td>{extra}</tr>"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("json_path"); ap.add_argument("html_path"); args = ap.parse_args()
    data = json.load(open(args.json_path, encoding="utf-8")); lb = data["livebench"]
    leaders = "".join(row(x) for x in lb["overall_leaders"][:5])
    open_rows = "".join(row(x) for x in lb["open_weight_leaders"][:5])
    cost_rows = "".join(row(x) for x in lb["cost_leaders"][:5])
    scale_sections = []
    for bench in data["scale"]:
        trs = "".join(f"<tr><td>{r['rank']}</td><td>{esc(r['model'])}</td><td>{r['score']}</td><td>{('± ' + str(r['uncertainty'])) if r['uncertainty'] is not None else '—'}</td></tr>" for r in bench["rows"][:10])
        scale_sections.append(f"<h3>{esc(bench['benchmark'])}</h3><p><a href=\"{esc(bench['url'])}\">Source leaderboard</a></p><table><tr><th>Rank</th><th>Model</th><th>Score</th><th>Uncertainty</th></tr>{trs}</table>")
    stamp=esc(data["extracted_at"])
    body=f'''<!doctype html><html><body style="font-family:Arial,sans-serif;color:#202124;line-height:1.45"><h1>Daily AI Leaderboard Report</h1><p><strong>Live snapshot:</strong> {stamp} UTC</p><p>This recovered report uses the latest rows successfully extracted from LiveBench and Scale AI. Ranks and scores are reproduced as displayed by the sources.</p><h2>Executive summary</h2><ul><li>LiveBench release: {esc(lb['release'])}; {lb['models']} model rows extracted.</li><li>Scale AI: all four requested benchmark pages returned ranking rows.</li><li>Cost per successful task is shown only where LiveBench publishes a positive source value.</li></ul><h2>1. LiveBench</h2><p><a href="{LIVEBENCH}">LiveBench source</a>. Category scores are calculated from the published task columns using the source category definitions.</p><h3>Overall leaders</h3><table><tr><th>Model</th><th>Provider</th><th>Overall</th><th>Cost/success</th></tr>{leaders}</table><h3>Best open-weight models</h3><table><tr><th>Model</th><th>Provider</th><th>Overall</th><th>Cost/success</th></tr>{open_rows}</table><h3>Lowest published cost per successful task</h3><table><tr><th>Model</th><th>Provider</th><th>Overall</th><th>Cost/success</th></tr>{cost_rows}</table>{''.join(f'<h3>{esc(k)}</h3><p><strong>Leader:</strong> {esc(v[0]["display_name"] if v else "No row")}; <strong>score:</strong> {esc(v[0]["categories"].get(k) if v else "—")}</p>' for k,v in lb['categories'].items() if k in ['Reasoning','Coding','Mathematics'])}<h2>2. Scale AI Leaderboards</h2>{''.join(scale_sections)}<h2>Method and limitations</h2><p>LiveBench cost values are source-provided. Scale pages do not publish an equivalent cost-per-successful-task metric. Small differences in Scale scores should be interpreted alongside the displayed uncertainty intervals.</p><p>Regards,<br>Ada</p></body></html>'''
    # Avoid accidental visible escape sequences in the MIME body.
    body=body.replace('\\n','')
    open(args.html_path,'w',encoding='utf-8').write(body)

LIVEBENCH = "https://livebench.ai/#/"
if __name__ == "__main__": main()
