# Continuous Improvement CI Manager Agent Specification

Status: production-ready design
Owner: manager-bot
Primary lane: #manager-hq
Execution lane: #ops-center / ops-bot
Risk lane: #admin-desk / admin-bot
Current as of: 2026-05-27 UTC

## Objective

Create an autonomous recurring Continuous Improvement (CI) Manager routine for OpenClaw that discovers existing operational reporting patterns, reuses their format and delivery paths, and produces actionable Infrastructure Utilisation & Efficiency Reports.

The agent should improve the system without adding chat noise. It reports only when there is a meaningful recommendation, a failed check, a stale workflow, or a measurable efficiency opportunity.

## Operating Model

The CI Manager is not a free-running chat participant. It is a scheduled manager routine that observes, summarizes, and routes work.

- `manager-bot` owns coordination, reporting, task ledger, and cross-lane recommendations.
- `ops-bot` owns implementation of monitoring, timers, logs, backups, health checks, and routine maintenance.
- `admin-bot` owns privileged changes: systemd changes, config mutation, permissions, credentials, service restarts, firewall/network changes, destructive cleanup.
- `security-bot` owns defensive security findings and authorized validation.
- Specialist agents own their own lane improvements once routed.

Default cadence:

- Daily utilisation report: 05:00 UTC, after maintenance and backup windows.
- Weekly trend report: Monday 05:30 UTC, aggregating daily logs.
- Immediate alert: only for failed backups, failed maintenance, unavailable gateway, credential exposure, storage exhaustion, or repeated routing failures.

The current OpenClaw environment already has daily patterns the CI Manager should mirror:

- `qmd-index`: around 03:00 UTC
- `maintenance`: around 04:00 UTC
- `github-backup`: around 04:30 UTC
- `agent-utilisation`: around 05:00 UTC

## Discovery Phase

Before producing or changing reports, the CI Manager runs discovery and writes a bounded discovery artifact under:

`/home/vin/.openclaw/logs/ci-manager-discovery-YYYY-MM-DDTHH:MM:SSZ.json`

Discovery inputs:

- `systemctl --user list-timers --all`
- known OpenClaw systemd units in backup snapshots
- `/home/vin/.openclaw/openclaw.json`
- `/home/vin/.openclaw/logs/*.log`
- `/home/vin/.openclaw/cron/jobs-state.json`, if present
- OpenClaw CLI checks: `openclaw health --json`, `openclaw config validate --json`, `openclaw cron list --json`, `openclaw agents bindings`
- delivery queue failures under `/home/vin/.openclaw/delivery-queue/failed`

Pattern matching requirements:

- Infer schedule order and avoid overlap with existing jobs.
- Reuse existing log naming: `ci-manager-YYYY-MM-DDTHH:MM:SSZ.log`.
- Reuse existing tone: concise plain text with short sections, not verbose dashboards.
- Reuse existing destination patterns; do not invent a new channel without approval.
- Identify whether reports are sent by Gmail, Discord, Telegram, or only written locally.
- Detect stale failed deliveries and channel/user targeting mistakes.

Discovery must redact or avoid printing tokens, API keys, OAuth material, gateway auth tokens, Discord tokens, Telegram bot tokens, and email secrets.

## Metrics Gathered

The CI Manager gathers metrics in four groups.

Compute and memory:

- Load average and CPU saturation trend.
- Process count and long-lived orphan candidates.
- Top memory consumers.
- Available RAM and swap pressure.
- OpenClaw event loop utilization, p99 delay, max delay, and degraded reasons.
- Model usage and session pressure where available.

Storage and backups:

- Disk usage by filesystem.
- Growth of `/home/vin/.openclaw/logs`, workspaces, sessions, backups, and media.
- Backup success/failure, latest commit id, and push status.
- Redundant historical backup candidates.
- Large generated artifacts without validation reports.
- Failed delivery queue size and age.

Network and channels:

- Gateway status and bind mode.
- Discord/Telegram channel configured/running/connected states.
- Tailscale status when installed and enabled.
- Transport failures, reconnect attempts, and last event/activity times.
- API latency or gateway timeout evidence from logs.

Agent management and workflow:

- Configured agents and Discord bindings.
- Missing or stale `SOUL.md`, `TOOLS.md`, `HEARTBEAT.md`, routing notes, or daily memory.
- Sessions with `abortedLastRun`, high token pressure, or repeated compactions.
- Cross-agent visibility or spawn restrictions that block manager handoffs.
- Stale routed tasks with no owner/status/next action.
- Specialist lanes receiving work outside their ownership.

## Report Contract

Each daily report must contain:

```text
OpenClaw CI Manager Report (YYYY-MM-DD UTC)

Executive status
- Overall: OK / Attention / Blocked
- Checks run:
- New findings:
- Repeated findings:
- Human action required:

Infrastructure utilisation
- Compute:
- Memory:
- Storage:
- Network/channels:
- Backup/maintenance:

Agent and workflow health
- Active agents:
- Routing/bindings:
- Stale tasks:
- Handoff blockers:
- Session pressure:

Recommendations
- P0:
- P1:
- P2:

Routed actions
- Owner:
  Task:
  Reason:
  Validation:
  Destination:

Evidence
- Logs:
- Commands:
- Artifacts:
```

Output rules:

- Write full logs locally.
- Send or post only a short summary unless there is a failure.
- Include exact timestamps and file paths.
- Separate facts, inferred trends, and recommendations.
- Never paste secrets or full config files into reports.
- Link or name local artifacts instead of dumping long JSON.

## Recommendation Severity

P0:

- Backup failed or no recent successful backup.
- Gateway unavailable or channels disconnected.
- Plaintext secrets exposed in broad-readable files.
- Disk projected to fill within 72 hours.
- Security-impacting config drift.

P1:

- Maintenance failed but gateway recovered.
- Repeated delivery queue failures.
- Cross-agent routing blocked.
- Sessions repeatedly aborting.
- Agent lane missing core identity/routing files.
- Logs or media growing unexpectedly.

P2:

- HEARTBEAT.md has no useful routine checks.
- Memory files stale.
- Optional timer or report format improvements.
- Backup or report logs need retention cleanup.
- Slicer/modeling/research/ops lane process improvements.

## Workflow and Orchestration

The CI Manager follows this loop:

1. Discover current operational patterns.
2. Gather metrics.
3. Compare against prior daily reports.
4. Classify findings by severity.
5. Route actions to the right owner.
6. Write local report and raw evidence.
7. Notify only when useful.
8. Record follow-up state for the next run.

State file:

`/home/vin/.openclaw/workspaces/manager-bot/memory/ci-manager-state.json`

State schema:

```json
{
  "lastRunAt": "2026-05-27T05:00:00Z",
  "lastReportPath": "/home/vin/.openclaw/logs/ci-manager-2026-05-27T05:00:00Z.log",
  "openFindings": [
    {
      "id": "ci-2026-05-27-001",
      "severity": "P1",
      "owner": "ops-bot",
      "summary": "Cross-agent visibility blocks manager handoff to modeler-bot.",
      "firstSeenAt": "2026-05-27T12:33:00Z",
      "lastSeenAt": "2026-05-27T12:33:00Z",
      "status": "open",
      "nextAction": "Preview config change or document direct-channel workaround."
    }
  ],
  "quietFindings": [
    "Findings suppressed because unchanged and non-urgent"
  ]
}
```

Routing template:

```text
Task:
Owner:
Priority:
Goal:
Context:
Constraints:
Deliverables:
Validation required:
Post result to:
Open questions/blockers:
```

The CI Manager must not perform privileged fixes directly. It may draft the exact task for `admin-bot` or `ops-bot`, including commands to preview, validation checks, and rollback notes.

## Safety Boundaries

Allowed without approval:

- Read logs, timers, OpenClaw config, workspace docs, session metadata, and backup status.
- Run non-mutating diagnostics.
- Write reports and state files in the manager workspace.
- Recommend routing changes and draft handoff messages.

Requires admin lane or explicit approval:

- Editing `/home/vin/.openclaw/openclaw.json`.
- Changing systemd units or timers.
- Restarting OpenClaw gateway or channels.
- Modifying credentials, SecretRefs, permissions, firewall, SSH, Tailscale, or service accounts.
- Deleting logs, backups, sessions, media, or generated artifacts.

Never do:

- Exfiltrate private config or tokens.
- Send reports externally to new destinations without approval.
- Clean up failed deliveries or backups destructively without a preview.
- Run active security scans without authorized scope.

## Implementation Plan

Phase 1: observe only

- Add CI Manager report script in `/home/vin/.openclaw/workspace/scripts/openclaw-ci-manager-report.sh`.
- Generate local logs only.
- Validate discovery output and report shape for three daily runs.
- Compare against existing `agent-utilisation` report and remove duplication.

Phase 2: route and notify

- Send concise summaries to the same destination used by current utilisation reporting.
- Route owner-specific findings into manager task ledger.
- Suppress unchanged P2 findings unless weekly report.

Phase 3: trend and optimization

- Add seven-day trends for disk, backup duration, maintenance duration, event loop delay, and session pressure.
- Add workflow efficiency recommendations: stale tasks, overloaded lanes, missing ownership, cross-agent communication failures.
- Add recommendation aging so repeated unresolved issues escalate.

Phase 4: controlled remediation

- For low-risk ops tasks, produce exact patches or commands for review.
- For admin tasks, route previews to `admin-bot` with validation and rollback.
- For security tasks, route to `security-bot` with explicit authorized scope.

## Acceptance Criteria

The CI Manager is production-ready when:

- It runs on schedule without overlapping maintenance or backup jobs.
- It writes local logs and state every run.
- It reports the same operational style as existing maintenance and backup logs.
- It identifies failed backups, failed maintenance, gateway/channel outages, and delivery queue failures.
- It flags agent workflow blockers, including cross-agent handoff restrictions.
- It routes recommendations to the correct lane using `ROUTING.md`.
- It does not leak secrets.
- It does not make privileged changes directly.
- It has a weekly trend view with repeated findings deduplicated.
- A failed run is visible in logs and does not break the gateway.

## Initial Known Findings To Track

- `modeler-bot` exists and is bound to `#modeling-studio`, but manager direct session send is blocked by session visibility policy.
- Manager session spawning is restricted to `manager-bot`, so cross-agent status probes require either direct channel routing or a config/policy change.
- There is an old failed delivery queue item from 2026-05-16 caused by user/channel targeting confusion.
- Maintenance logs have reported plaintext secret-bearing config fields in `openclaw.json`; migration to SecretRefs remains admin/security work.
- The existing daily utilisation report at 05:00 UTC is a strong base; CI Manager should extend or replace it rather than create duplicate noise.

## Example Daily Summary

```text
OpenClaw CI Manager Report (2026-05-27 UTC)

Executive status
- Overall: Attention
- Checks run: health, config validate, cron list, timers, backup log, maintenance log, delivery queue, agent bindings
- New findings: manager cannot directly probe modeler-bot due to session visibility restrictions
- Repeated findings: plaintext secret-bearing config fields still need SecretRefs migration
- Human action required: none unless you want cross-agent manager handoffs restored

Recommendations
- P1 ops/admin: review tools.sessions.visibility or equivalent policy needed for manager-bot cross-agent handoffs
- P1 ops: inspect failed delivery queue item from 2026-05-16 and confirm no retry loop remains
- P2 manager: fold CI Manager output into existing 05:00 utilisation report to avoid duplicate reports
```
