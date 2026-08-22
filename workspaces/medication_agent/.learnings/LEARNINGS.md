# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

## 2026-08-21 - Medication reminder source of truth

- Category: correction
- Lesson: medication reminders must come from a durable schedule manifest, not from reconstructing partial channel history or live search results.
- Failure mode: losartan was omitted from the `2026-08-21` medication reminder because the agent had no saved reminder jobs and no workspace memory for the schedule, so it recovered only part of the list.
- Guardrail: verify every medication has a concrete next trigger date in `REMINDER_SCHEDULE.md` before posting the reminder channel update.

---
