# Heartbeat checklist

Run read-only; report only genuine failures.
- Check gateway health and openclaw-* timers for failed or missed runs.
- Scan the latest maintenance/backup logs for new errors and treat transient health-gate noise as diagnostics first.
- Review .learnings/ and memory for durable ops lessons; record one concise item when evidenced.
