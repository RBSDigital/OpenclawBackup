# Self-Improvement Routine

This workspace uses a lightweight autonomous review loop:

1. Capture problems and corrections immediately in `.learnings/`.
2. Review recent entries on a schedule, ideally every 6 hours.
3. Promote repeated, broadly useful items into the right durable file.
4. Auto-promote only low-risk, non-sensitive fixes.
5. Keep safety- or routing-affecting changes reviewable by a human.

## What To Log

- Command failures and tool errors -> `.learnings/ERRORS.md`
- User corrections and better approaches -> `.learnings/LEARNINGS.md`
- Missing capabilities or standing asks -> `.learnings/FEATURE_REQUESTS.md`

## Promotion Checklist

- [ ] Is this issue repeated, not one-off?
- [ ] Is it broadly useful beyond the current session?
- [ ] Is it safe to store as a durable note?
- [ ] Does it belong in the right target file?
- [ ] Should it be summarized rather than copied verbatim?
- [ ] Is it safe to auto-apply without changing safety, routing, permissions, or external actions?

## Promotion Targets

- Workflow changes -> `AGENTS.md`
- Tool gotchas -> `TOOLS.md`
- Behavior and agent style -> `SOUL.md`
- Stable facts and preferences -> `MEMORY.md` in main sessions only

## Autonomy Rules

- Log first, improve second.
- Prefer summaries over raw transcripts.
- Do not store secrets, tokens, or private raw data.
- Do not auto-apply routing or safety changes without review.
- Low-risk documentation, wording, checklists, routing hints, and tooling notes can be auto-promoted when they are repeated and clearly non-sensitive.

## Review Prompt

Use this prompt for the autonomous review run:

```text
Review recent `.learnings` entries across all agent workspaces (found under `~/.openclaw/workspaces/*/.learnings/`) and identify repeated failures, corrections, and feature requests.

Tasks:
- summarize new items since the last review
- cluster repeated issues by pattern
- suggest the smallest durable fix for each repeated pattern
- identify anything that should be promoted to AGENTS.md, TOOLS.md, SOUL.md, or MEMORY.md
- auto-promote repeated low-risk fixes when they are clearly non-sensitive
- if there is no new signal, say so briefly and stop

Constraints:
- do not expose secrets or raw transcripts
- do not rewrite durable files unless explicitly approved
- prefer short bullet points
- keep the output actionable
```
