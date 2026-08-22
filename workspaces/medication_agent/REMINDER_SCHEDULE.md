# Medication Reminder Schedule

Source of truth for the `#medication-reminders` channel.

## Rules

- Every medication on the active list must have an explicit next trigger date before a reminder is posted.
- If a medication has no confirmed date, pause and repair the schedule instead of omitting it.
- Channel posts should include all medications that are due for that run, not just the first item recovered from chat history.

## Current Trigger Dates

- `Atorvastatin 20mg tablets` - `2026-08-14 09:00 UTC` - `28 day` cycle
- `Amlodipine 5mg tablets` - `2026-08-21 09:00 UTC` - `56 day` cycle
- `Losartan 100mg tablets` - `2026-08-21 09:00 UTC` - `56 day` cycle
- `Indapamide 1.5mg modified-release tablets` - `2026-08-29 09:00 UTC` - `56 day` cycle
- `Mounjaro KwikPen 5mg/0.6ml` - `2026-08-29 09:00 UTC` - `56 day` cycle
- `Metformin 500mg modified-release tablets` - `2026-09-11 09:00 UTC` - `56 day` cycle
- `GlucoRx CarePoint hypodermic insulin needles` - `2028-07-12 09:00 UTC` - provisional `100 week` fallback until the actual first-prescribed date is provided

## Notes

- The losartan omission on `2026-08-21` happened because the reminder set was being reconstructed from partial channel history instead of a durable schedule manifest.
- The fix is to keep this file up to date and require a full list check before every reminder post.
