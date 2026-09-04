# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

## 2026-08-21 - Medication reminder source of truth

- Category: correction
- Lesson: medication reminders must come from a durable schedule manifest, not from reconstructing partial channel history or live search results.
- Failure mode: losartan was omitted from the `2026-08-21` medication reminder because the agent had no saved reminder jobs and no workspace memory for the schedule, so it recovered only part of the list.
- Guardrail: verify every medication has a concrete next trigger date in `REMINDER_SCHEDULE.md` before posting the reminder channel update.

---

## 2026-09-03 - Medication reminder delivery target

- Category: correction
- Lesson: reminder posts must target `#medication-reminders` explicitly, not the currently active lane or `#manager-hq` default.
- Failure mode: the 2026-08-29 reminder content was published in `#manager-hq` instead of the medication channel, so it looked like it never reached the reminder lane.
- Guardrail: check the destination channel before sending and use `channel:1537422220391874590` for medication reminders.

---
