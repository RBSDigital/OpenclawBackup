# Errors

Command failures and integration errors.

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
