# ITC Improvement Measurement Scorecard

## Purpose

This scorecard provides a practical way to track whether improvement actions are working. It combines leading indicators, which show whether the team is changing behaviour, and lagging indicators, which show whether outcomes are improving.

## Measurement Principles

- Use a small number of useful measures.
- Track trends rather than one-off snapshots.
- Pair every metric with an owner and review cadence.
- Avoid metrics that incentivise shallow compliance without improving delivery.
- Use evidence from source artefacts such as ADO, SharePoint/Drive, RAID logs, action trackers, and sprint records.

## Suggested Scorecard

| Theme | Metric | Type | Target Direction | Review Cadence | Evidence Source |
| --- | --- | --- | --- | --- | --- |
| Deployment troubleshooting | Mean time to diagnose deployment issues | Lagging | Down | Monthly | Incident / deployment log |
| Deployment troubleshooting | Integrations with current runbook | Leading | Up | Monthly | Integration runbook register |
| Architecture documentation | Systems/integrations with current architecture docs | Leading | Up | Monthly | Architecture document register |
| Architecture documentation | Repeated architecture review findings | Lagging | Down | Monthly | Architecture review notes |
| Technical debt | Open technical debt age | Lagging | Down | Monthly | ADO debt backlog |
| Technical debt | Debt items with owner/impact/priority | Leading | Up | Monthly | ADO fields |
| ADO / SharePoint hygiene | Tickets meeting definition of ready | Leading | Up | Weekly | ADO sampling |
| ADO / SharePoint hygiene | Stale tickets older than threshold | Lagging | Down | Weekly | ADO dashboard |
| Due dates / dependencies | Active work items with due dates | Leading | Up | Weekly | ADO dashboard |
| Due dates / dependencies | Average dependency resolution time | Lagging | Down | Monthly | Dependency tracker |
| Delivery artefacts | Active initiatives with required artefacts | Leading | Up | Monthly | SharePoint/Drive audit |
| Delivery artefacts | Overdue actions | Lagging | Down | Weekly | Action tracker |
| Sprint retros/reviews | Retrospective action closure rate | Lagging | Up | Fortnightly | Retro action log |
| Sprint retros/reviews | Sprint review attendance | Leading | Up | Fortnightly | Attendance record |
| Communication clarity | Sampled tickets passing quality standard | Leading | Up | Weekly | Ticket quality sample |
| Communication clarity | Rework linked to unclear requirements | Lagging | Down | Monthly | Defect/rework log |
| Stakeholder collaboration | Unresolved stakeholder decisions | Lagging | Down | Weekly | Decision log |
| Stakeholder collaboration | Stakeholder satisfaction pulse | Lagging | Up | Monthly | Pulse survey |
| Responsiveness | Acknowledgement time by priority | Lagging | Down | Weekly | Intake tracker |
| Responsiveness | Overdue responses | Lagging | Down | Weekly | Service request dashboard |
| Meeting discipline | Meetings with agenda and minutes | Leading | Up | Monthly | Meeting audit |
| Meeting discipline | Action closure rate by forum | Lagging | Up | Monthly | Action tracker |

## Baseline Approach

1. Establish a four-week baseline for each metric where data exists.
2. For missing data, start with a manual sample rather than waiting for perfect automation.
3. Agree Red / Amber / Green thresholds after the first baseline.
4. Review the scorecard monthly and retire metrics that do not drive useful decisions.

## Example RAG Thresholds

Ticket hygiene:
- Green: 90% or more sampled tickets meet standard.
- Amber: 70-89%.
- Red: below 70%.

Overdue actions:
- Green: fewer than 5 overdue actions.
- Amber: 5-10 overdue actions.
- Red: more than 10 overdue actions or any high-priority action overdue by more than two weeks.

Architecture documentation:
- Green: 90% or more critical systems/integrations have current docs.
- Amber: 70-89%.
- Red: below 70%.

Dependency tracking:
- Green: 95% or more dependencies have owner and need-by date.
- Amber: 80-94%.
- Red: below 80%.

## Governance Cadence

Weekly delivery review:
- Overdue actions.
- Open high risks/issues.
- Blocked dependencies.
- Ticket hygiene exceptions.

Fortnightly sprint review / retrospective:
- Sprint review attendance.
- Retrospective action closure.
- Repeated improvement themes.

Monthly continuous improvement review:
- Full scorecard.
- Technical debt trend.
- Architecture documentation coverage.
- Stakeholder feedback.
- Decisions and escalations.

Quarterly reset:
- Confirm whether metrics still matter.
- Refresh thresholds.
- Review whether artefacts are helping or creating noise.
- Agree next quarter improvement focus.

