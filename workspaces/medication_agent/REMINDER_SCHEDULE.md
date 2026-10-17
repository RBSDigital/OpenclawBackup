# Medication Reminder Schedule

Source of truth for the `#medication-reminders` channel.

## Rules

- Every medication on the active list must have an explicit next trigger date before a reminder is posted.
- If a medication has no confirmed date, pause and repair the schedule instead of omitting it.
- Channel posts should include all medications that are due for that run, not just the first item recovered from chat history.

## Current Trigger Dates

- `Atorvastatin 20mg tablets` - `2026-10-30 09:00 UTC` - `28 day` cycle
- `Amlodipine 5mg tablets` - `2026-11-27 09:00 UTC` - `56 day` cycle
- `Losartan 100mg tablets` - `2026-11-27 09:00 UTC` - `56 day` cycle
- `Indapamide 1.5mg modified-release tablets` - `2026-10-20 09:00 UTC` - `56 day` cycle
- `Mounjaro KwikPen 5mg/0.6ml solution for injection` - `2026-10-20 09:00 UTC` - weekly injection / `2 pens` supply
- `Metformin 500mg modified-release tablets` - `2026-10-30 09:00 UTC` - `56 day` cycle
- `GlucoRx CarePoint hypodermic insulin needles for pre-filled / reusable pen injectors` - `2026-10-29 09:00 UTC` - `100 needles` supply; cadence remains provisional pending prescribing history

## Notes

- The losartan omission on `2026-08-21` happened because the reminder set was being reconstructed from partial channel history instead of a durable schedule manifest.
- The fix is to keep this file up to date and require a full list check before every reminder post.
- NHS app confirmation on `2026-10-16` supplied the next permitted dates for every active item: Amlodipine and Losartan `2026-11-27`; Atorvastatin and Metformin `2026-10-30`; Indapamide and Mounjaro `2026-10-20`; and GlucoRx needles `2026-10-29`. These are the earliest permitted reminder dates, set at `09:00 UTC`.
