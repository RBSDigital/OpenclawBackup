# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Multi-Agent Notes

- `ops-bot`: Operational status, incident summaries, alerts, maintenance posture, and backup coverage checks.
- `admin-bot`: Privileged admin workflows and high-risk infrastructure/account changes.
- `researcher-bot`: Source-heavy research, investigation, and synthesis.

When checking backups or maintenance, verify the active agent list first if a local OpenClaw inventory tool is available. Coverage should include each active agent's workspace, memory, tool notes, heartbeat state, scheduler/cron definitions, and restore-critical OpenClaw state/config. Do not expose another agent's private memory in shared channels.

## Shared Agent Memory Vault

- Path: `/home/vin/ObsidianVaults/AdaKTVault/06_system/agent-memory-vault`
- Primary folders: `Ops/`, `Decisions/`, `Manager/`
- Promote reusable operational procedures and maintenance findings only after sanitizing secrets and private context.

## Related

- [Agent workspace](/concepts/agent-workspace)
