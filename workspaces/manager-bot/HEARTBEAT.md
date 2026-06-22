```markdown
# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.
```

## Manager Heartbeat Checklist

- Follow `COST_POLICY.md`: batch checks, use cheap deterministic tools first, and stay quiet unless there is signal.
- Review open Discord tasks across `#manager-hq`, `#research-lab`, `#ops-center`, `#admin-desk`, `#modeling-studio`, and `#security-lab`, then summarize owner, status, blocker, and next action.
- Check routing and keep one lightweight lane check per active specialist lane; note intentionally idle lanes and fold any stale-memory review for `ops-bot`, `security-bot`, or `modeler-bot` into the same heartbeat so the lane never goes empty.
- Keep private memory isolated from shared Discord channels, triage `/home/vin/ObsidianVaults/AdaKTVault/06_system/agent-memory-vault/Inbox`, and review recent `memory/YYYY-MM-DD.md` files for anything that belongs in private `MEMORY.md` or the shared Agent Memory Vault.

## Cost Discipline

- Skip repeat checks when the same source was checked recently and nothing new triggered them.
- Prefer counts, timestamps, and exact changed items over broad transcript or file reads.
- Do not load private `MEMORY.md` during shared Discord heartbeats.
- Reply `HEARTBEAT_OK` when nothing changed.

## Related

- [Heartbeat config](/gateway/config-agents)
