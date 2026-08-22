---
owner: manager-bot
created: 2026-08-21
last_verified: 2026-08-21
status: accepted
confidence: medium
source: manager-bot analysis of medication reminder miss
tags:
  - durable-memory
  - medication
  - reminders
  - discord
---

# Losartan Reminder Fix

## Summary

Losartan was missed in the `#medication-reminders` run because the medication agent had no durable schedule manifest or saved reminder jobs to consult, so it reconstructed the reminder set from partial channel history and posted an incomplete list.

## Fix

- Added `REMINDER_SCHEDULE.md` in the medication workspace as the source of truth.
- Added a guardrail in medication-agent instructions to verify every medication has an explicit trigger date before posting.
- Logged the failure mode in `.learnings/LEARNINGS.md` so future reviews catch it.

## Current Rule

- Do not post a medication reminder unless every medication on the active list has a concrete next trigger date.
- If the schedule is incomplete, repair the manifest first instead of omitting the missing medication.

## Coverage

- Confirmed scheduled items: amlodipine, losartan, indapamide, Mounjaro, metformin, atorvastatin.
- Provisional fallback item: GlucoRx needles, pending the actual first-prescribed date.

## Related

- `medication_agent`
- `#medication-reminders`
- `manager-bot`

## Indexing

- Re-embedding the vault was attempted with `qmd`, but the local `better-sqlite3` native module/build setup failed under Node 24.18.0, so the note is written and the index refresh remains a follow-up task.
