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

## Shared Agent Memory Vault

- Path: `/home/vin/ObsidianVaults/AdaKTVault/06_system/agent-memory-vault`
- Purpose: shared sanitized durable memory for cross-agent recall.
- Manager responsibility: maintain `00_Index/`, routing memory, promotion rules, and periodic inbox triage.
- Retrieval status: the live vault is indexed with `qmd` as collection `ada_kt_vault`; re-run `qmd collection add /home/vin/ObsidianVaults/AdaKTVault --name ada_kt_vault --mask '**/*.md'` and `qmd embed` if the index is missing or stale.
- Obsidian status: Markdown vault is usable now; OpenClaw `obsidian` skill requires the official `obsidian` CLI binary on `PATH`.

## Discord Connector

- When multiple messaging backends are configured, read a Discord lane with `channel="discord"` and `target="channel:<discord-channel-id>"`.
- Do not pass the Discord ID through `channelId`; the connector expects the encoded `target`.

## Structurizr

- If `structurizr-cli` is not on `PATH`, use a portable Java 17 runtime plus the official CLI ZIP.
- Prefer `validate -workspace workspace.dsl` followed by `export -workspace workspace.dsl -format mermaid -output out` for local verification.
- Docker-based validation may fail when the current user cannot reach `unix:///var/run/docker.sock`.

## Related

- [Agent workspace](/concepts/agent-workspace)
