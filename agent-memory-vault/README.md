# Agent Memory Vault

Shared, sanitized durable memory for the OpenClaw agent team.

This vault is for reusable facts, decisions, procedures, source notes, project context, and cross-agent coordination memory. It is not a transcript archive and it is not a replacement for each agent's private `MEMORY.md`.

## Rule

Only promote information here when it is useful beyond the current conversation and safe to share across agents.

Do not store:
- Secrets, tokens, credentials, private keys, session cookies, or auth material.
- Raw private chats, full transcripts, or personal context that belongs only in a private agent memory.
- Another agent's `MEMORY.md`, `USER.md`, `SOUL.md`, or private workspace notes.
- Unverified claims without a source, owner, date, or confidence.

## Memory Flow

1. Capture raw activity in `memory/YYYY-MM-DD.md` inside the relevant agent workspace.
2. Summarize durable lessons into that agent's long-term `MEMORY.md` when private or identity-related.
3. Promote sanitized reusable knowledge into this vault when it should be shared.
4. Link related notes and update `last_verified` when facts change.

## Folder Owners

- `Manager/` - manager-bot: routing memory, task ledger conventions, multi-agent operating model.
- `Research/` - researcher-bot: source-grounded findings, reusable research briefs, source registers.
- `Ops/` - ops-bot: operational procedures, status patterns, maintenance notes.
- `Security/` - security-bot: defensive security procedures, scope rules, report patterns.
- `Modeling/` - modeler-bot: 3D-print workflows, toolchain notes, artifact conventions.
- `Admin/` - admin-bot: audited admin runbooks only, no credentials.
- `Decisions/` - cross-agent decisions and architecture choices.
- `Sources/` - reusable source notes and verification references.
- `Inbox/` - temporary landing zone for notes that still need triage.

## Obsidian Status

The vault is ready as Markdown now. The OpenClaw `obsidian` skill becomes available once the official Obsidian CLI binary is installed and registered on `PATH`.
