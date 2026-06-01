# Operating Model

The vault is a shared memory layer for agents, coordinated by `manager-bot`.

## Responsibilities

- `manager-bot` owns index quality, routing memory, cross-agent summaries, and promotion discipline.
- Specialist agents own their lane folders and should write only sanitized durable notes.
- `admin-bot` should use this vault only for audited procedures and decisions, not sensitive state.
- `security-bot` may document defensive procedures, scopes, and sanitized findings, but not live secrets or exploit-enabling detail outside authorized reports.

## Recall Pattern

Before a substantial task, agents should check:

1. Their own workspace instructions and local memory.
2. This vault's relevant folder.
3. `Decisions/` for prior cross-agent choices.
4. `Sources/` for reusable source notes.

## Write Pattern

When adding a note:

- Use a template from `Templates/`.
- Include `owner`, `created`, `last_verified`, `confidence`, and `status`.
- Prefer concise distilled notes over logs.
- Link related notes.
- Keep raw artifacts in the task workspace unless they are intentionally promoted.
