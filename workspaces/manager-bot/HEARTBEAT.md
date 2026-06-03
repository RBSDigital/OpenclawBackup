```markdown
# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.
```

## Manager Heartbeat Checklist

When heartbeats are enabled, use them to keep the multi-agent setup tidy:

- Follow `COST_POLICY.md`: batch checks, use cheap deterministic tools first, and stay silent unless there is signal.
- Review open Discord tasks across `#manager-hq`, `#research-lab`, `#ops-center`, `#admin-desk`, `#modeling-studio`, and `#security-lab`.
- Summarize owner, status, blocker, and next action for active work.
- Check whether specialist work is being executed in the right lane.
- Nudge stale routed tasks only when there is a real blocker or user-visible delay.
- Keep private memory isolated from shared Discord channels.
- Triage `/home/vin/ObsidianVaults/AdaKTVault/06_system/agent-memory-vault/Inbox` periodically and promote sanitized durable notes into the right vault folder.
- Review recent `memory/YYYY-MM-DD.md` files periodically and decide whether anything belongs in private `MEMORY.md` or the shared Agent Memory Vault.

## Cost Discipline

- If the last heartbeat checked the same source recently and there is no new trigger, skip it.
- Prefer counts, timestamps, and exact changed items over broad transcript/file reads.
- Do not load private `MEMORY.md` during shared Discord heartbeats.
- Reply `HEARTBEAT_OK` when nothing changed.

## Related

- [Heartbeat config](/gateway/config-agents)
