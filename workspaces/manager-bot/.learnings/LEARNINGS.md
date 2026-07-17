# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

---

## [LRN-20260716-001] best_practice

**Logged**: 2026-07-16T10:21:00Z
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
Installed skill registry slugs do not always match the informal request names, so verify the actual ClawHub slug before installing or documenting usage.

### Details
For this task, "Browser Control" mapped to `browser-control`, "Composio" mapped to `composio`, and "URL-to-Markdown" mapped to `url2md`. The browser-control skill exposes a remote VNC/ngrok workflow, Composio requires an API key and begins with `COMPOSIO_SEARCH_TOOLS`, and `url2md` provides a direct local HTML-to-Markdown conversion path.

### Suggested Action
When a user gives a capability name, confirm the registry slug with `clawhub search` or `clawhub inspect` before treating the skill as installed or ready.

### Metadata
- Source: conversation
- Tags: clawhub, skills, installation, documentation
- First-Seen: 2026-07-16
- Last-Seen: 2026-07-16

## [LRN-20260716-002] insight

**Logged**: 2026-07-16T10:52:00Z
**Priority**: high
**Status**: pending
**Area**: ops

### Summary
Gateway health failures can coexist with successful backup/report completion if the pipelines keep diagnostic artifacts and do not hard-fail on a single transient availability check.

### Details
On 2026-07-16, the maintenance run retried the post-update health gate 13 times, attempted a recovery reinstall, and still ended with the gateway stopped after repeated crashes. The backup run still completed and pushed commit `ad00496` while recording `openclaw cron list failed` and `openclaw health failed` as diagnostic warnings.

### Suggested Action
Keep health gating strict for availability, but make recovery/report flows resilient: capture diagnostics, continue backups when safe, and inspect gateway/systemd logs after `1006 abnormal closure` or repeated crash states instead of blindly retrying forever.

### Metadata
- Source: incident logs
- Tags: ops, gateway, health, backup, diagnostics, resilience
- First-Seen: 2026-07-16
- Last-Seen: 2026-07-16

---
