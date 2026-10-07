# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

## [LRN-20261006-001] tube-branch-verification

**Logged**: 2026-10-06T11:42:00Z
**Priority**: medium
**Status**: applied
**Area**: travel

### Summary
Tube route advice incorrectly presented Richmond as the required District-line destination for Chiswick Park. The official TfL timetable confirms Chiswick Park is reached on the westbound District service towards Ealing Broadway; branch and stop validation must be explicit.

### Action
For time-sensitive public-transport advice, verify the exact origin, destination, departure/arrival interpretation, line branch, train destination, intermediate stops and live service status against TfL before giving timed steps. If multiple branches serve a shared section, state the safest exact destination and explain alternatives rather than asserting one without checking.

### Metadata
- Source: user correction and TfL timetable verification
- Tags: travel, TfL, District-line, branch-selection, route-validation

---

## [LRN-20260930-001] supported-runtime-status-tools

**Logged**: 2026-09-30T18:20:00Z
**Priority**: medium
**Status**: applied
**Area**: automation

### Summary
The daily utilisation report repeatedly referenced unsupported CLI commands for session and cron status, even though supported runtime tools were available.

### Action
Use runtime session-status telemetry, sessions list/history, and the automations status/list tools. Do not invoke or report unsupported CLI commands as blockers.

### Metadata
- Source: recurring report blocker
- Tags: utilisation, cron, session-status, tooling

---

## [LRN-20260917-001] source-specific-retrieval

**Logged**: 2026-09-17T09:32:00Z
**Priority**: high
**Status**: applied
**Area**: automation

### Summary
Leaderboard automation must use source-specific retrieval and validation. HTTP 200/404 alone is not evidence that rankings were or were not available: a static asset can be reachable through direct HTTP while a generic client is blocked or served a shell page.

### Action
Use browser-like headers and retries, discover current release assets, parse known detail pages, require ranking rows from every requested source, and update snapshots only after verified email delivery.

### Metadata
- Source: incident reproduction
- Tags: leaderboard, extraction, validation, email, automation

---

## [LRN-20260914-001] best_practice

**Logged**: 2026-09-14T08:42:00Z
**Priority**: high
**Status**: pending
**Area**: automation

### Summary
Scheduled research jobs must distinguish technical run completion from successful business outcome and must verify both extraction and email delivery.

### Details
The leaderboard job reported `ok` at the scheduler level even though it neither produced a trusted report nor sent a warning email. The catch-up run succeeded after using live source retrieval and the gateway Gmail path.

### Suggested Action
Treat report preparation and delivery as explicit success gates. Do not mark a run complete, update the snapshot, or suppress failure notification until source extraction is reliable and the email send operation succeeds.

### Metadata
- Source: incident
- Tags: automation, research, email, delivery, observability
- Pattern-Key: [REDACTED_SECRET]
- Recurrence-Count: 1

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
