---
owner: manager-bot
created: 2026-08-20
last_verified: 2026-08-20
status: accepted
confidence: medium
source: manager-bot summary of live medication schedule
tags:
  - durable-memory
  - medication
  - reminders
  - discord
---

# Medication Reminder Service

## Summary

The medication reminder service is an OpenClaw-managed Discord workflow that posts concise reminder/order prompts for the medication lane.

## Details

- The medication lane is bound to Discord channel `1537422220391874590`.
- Active reminder jobs are enabled and currently idle between runs.
- Current reminder set includes amlodipine, losartan, indapamide, Mounjaro, metformin, atorvastatin, and insulin needles.
- The service posts concise reminders with dosage, quantity, and postage guidance rather than long explanations.
- Reorders are handled as separate medication order requests for some items, while others are reminder-only prompts.

## Related

- `manager-bot`
- `medication_agent`
- `#manager-hq`

## Review Notes

- Next review: when the medication schedule changes or a reminder job is added/removed
- Staleness risk: medium, because the medication list and timing can change
