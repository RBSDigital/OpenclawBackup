# Errors

Command failures and integration errors.

---

## [ERR-20260917-002] interpreter-name

**Logged**: 2026-09-17T09:00:00Z
**Priority**: low
**Status**: resolved
**Area**: tooling

### Summary
A diagnostic probe used `python`, which is not installed on this host.

### Fix
Use `python3` explicitly in extraction and diagnostic commands.

---

## [ERR-20260917-001] leaderboard-extraction

**Logged**: 2026-09-17T09:32:00Z
**Priority**: high
**Status**: resolved
**Area**: automation

### Summary
The daily job received unusable source responses: the LiveBench asset path was treated as 404 and Scale returned a shell/block page. Direct browser-like HTTP retrieval showed the LiveBench assets were 200 and Scale detail pages returned full ranking rows.

### Root Cause
The scheduled extraction relied on a lightweight generic fetch path without deterministic browser headers, retries, release discovery, or a hard ranking-row validation gate.

### Fix
Added `scripts/ai_leaderboard_extract.py` with browser-like headers, retries, LiveBench release/assets discovery, CSV/JSON aggregation, Scale detail-page parsing, and zero-row failure validation. The automation now requires this extractor before report generation and delivery.

### Metadata
- Reproducible: yes
- Related Files: scripts/ai_leaderboard_extract.py, state/ai-leaderboard-snapshot.json

---

## [ERR-20260914-001] daily-leaderboard-automation

**Logged**: 2026-09-14T08:42:00Z
**Priority**: high
**Status**: pending
**Area**: automation

### Summary
The 08:00 UTC leaderboard job reached both sites but could not reliably extract JavaScript-rendered results and had no Gmail-capable tool in its isolated tool policy, so no report or warning email was sent.

### Context
- Automation: Daily AI leaderboard capability report
- The run was marked technically successful despite its internal summary reporting failure.
- Delivery was not requested because the job had no usable report output.

### Suggested Fix
Expose the gateway/Gmail execution capability to the isolated job and require deterministic fallbacks for JavaScript-rendered sources, including direct static asset or rendered-page extraction.

### Metadata
- Reproducible: yes
- Related Files: state/ai-leaderboard-snapshot.json

---
