# Heartbeat Checklist

Use heartbeats for lightweight operational maintenance. Keep checks quiet unless there is risk, action needed, or useful status to report.

## Routine Checks

- Review recent ops messages for incidents, deployments, alerts, or unresolved requests.
- Check whether any scheduled backup or maintenance routine has failed, gone stale, or stopped reporting.
- Confirm the multi-agent setup still has clear ownership: `ops-bot` for ops/status, `admin-bot` for privileged changes, `researcher-bot` for source-heavy research.
- Verify backup coverage accounts for every active agent workspace, including instructions, memory files, tool notes, heartbeat state, and restorable OpenClaw state/config.
- Look for stale sessions, stuck background jobs, failed heartbeats, or duplicate responsibilities across agents.
- Update `memory/YYYY-MM-DD.md` after notable operational changes or maintenance findings.

## Related

- [Heartbeat config](/gateway/config-agents)
