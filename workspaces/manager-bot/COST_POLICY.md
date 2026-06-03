# API Token Cost Policy

Use this policy to keep agent work effective while minimizing API token spend.

## Default Principle

Spend tokens on judgment, not rediscovery. Prefer cheap deterministic tools, narrow context, durable memory, and explicit routing before using high-reasoning model calls.

## Routing Tiers

- **Tier 0: No model call where possible.** Use shell tools, local scripts, `rg`, `git`, `jq`, configured CLIs, and exact API queries for factual inspection, status checks, file search, formatting, and mechanical transforms.
- **Tier 1: Small model call.** Use for classification, short summaries, routing decisions, heartbeat triage, simple Discord replies, and low-risk formatting.
- **Tier 2: Standard reasoning.** Use for multi-step work where context is bounded and the action is reversible: normal code edits, docs updates, lightweight investigation, and specialist handoffs.
- **Tier 3: High reasoning / specialist execution.** Use only when the task needs deep design judgment, complex debugging, source synthesis, security-sensitive reasoning, financial judgment, or irreversible/high-impact recommendations.

## Runtime Defaults

- Default model alias `GPT`: `openai/gpt-5.4-mini`.
- Cheap model alias `GPT_CHEAP`: `openai/gpt-5.4-nano`.
- Cheap reasoning alias `REASONING_CHEAP`: `openai/o4-mini`.
- Full escalation alias `GPT_FULL`: `openai/gpt-5.5`.
- Fallback model: `openai/gpt-5.5`.

Use the full escalation model only when the task needs it. The gateway may need a restart/reload after model config changes.

## Context Budget Rules

- Start with search results, filenames, diffs, and exact excerpts instead of whole files or transcripts.
- Load only the skill file needed for the task; follow referenced files selectively.
- In handoffs, pass task, owner, goal, constraints, deliverables, validation, and exact links/files. Do not pass raw chat history unless it is essential.
- Summarize long outputs before handing them to another agent.
- Reuse durable memory for stable facts instead of rediscovering them.

## Delegation Rules

- Manager-bot keeps intake, triage, and status in `#manager-hq`.
- Route specialist work only once, with one clear owner.
- Avoid spawning multiple agents to inspect the same files, docs, or logs unless comparing independent approaches is explicitly useful.
- Ask for confirmation before starting detached work likely to run long, use expensive models, or touch high-risk systems.

## Heartbeat Rules

- Batch periodic checks into one heartbeat pass.
- Stay silent unless there is a meaningful change, blocker, urgent event, or useful summary.
- Skip checks that ran recently unless the trigger is urgent.
- Promote durable sanitized facts to the shared vault so later heartbeats do not repeat discovery.

## Spend Review

During periodic maintenance, look for repeat cost leaks:

- Long context loads that could become memory notes or indexes.
- Heartbeats that produce no action but still do heavy work.
- Specialist agents receiving broad prompts instead of bounded briefs.
- Repeated research of stable facts.
- High-reasoning calls used for simple routing, summaries, or tool-driven checks.

When a repeat leak is found, fix it by adding a script, checklist, memory note, routing rule, or tighter prompt pattern.
