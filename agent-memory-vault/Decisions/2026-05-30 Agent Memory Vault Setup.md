---
owner: manager-bot
created: 2026-05-30
last_verified: 2026-05-30
status: accepted
confidence: high
source: Vincent request in #manager-hq
tags:
  - decision
  - memory
  - obsidian
---

# Agent Memory Vault Setup

## Decision

Create `/home/vin/ObsidianVaults/AdaKTVault/06_system/agent-memory-vault` as the shared sanitized durable memory layer for the OpenClaw agent team.

## Rationale

The existing memory model is mostly per-agent files: `AGENTS.md`, `SOUL.md`, `TOOLS.md`, daily `memory/YYYY-MM-DD.md`, private `MEMORY.md`, and `.learnings/`. That is useful but fragmented. A shared vault gives agents a common place for durable, sanitized, linked recall without exposing private memory.

## Scope

This vault is for cross-agent recall only. Private or sensitive facts remain in the relevant agent workspace.

## Obsidian Status

The vault is Markdown-first and ready immediately. The OpenClaw `obsidian` skill remains unavailable until the official Obsidian CLI binary is installed and registered on `PATH`.

## Follow-Up

- Install/register official Obsidian CLI when a GUI-capable Obsidian app environment is available.
- Keep `admin-bot` limited to audited runbooks and decisions.
- Review `Inbox/` periodically during manager heartbeat cycles.
