# ITC Continuous Improvement Research and Remediation Plan

## Purpose

This document translates the feedback points into actionable remediation ideas, suggested artefacts, and measurable improvement indicators. The goal is to move from general feedback to repeatable management controls.

## 1. Deployment Troubleshooting Difficulty

Feedback observed:
- Improve integration documentation for WE scope.
- Improve CRM configuration for WE scope.

Research focus:
- Deployment troubleshooting usually degrades when support teams lack a single source of truth for environment dependencies, integration contracts, configuration ownership, and known failure modes.
- CRM and integration issues often need both functional context and technical traceability: business process, upstream/downstream systems, interface contracts, data mappings, credentials, queues, and release history.

Remediation ideas:
- Create an integration support runbook for each WE integration.
- Create a CRM configuration catalogue for WE-owned configuration.
- Add deployment rollback and validation checklists.
- Maintain a known errors and fixes log linked to incidents and releases.

Suggested artefacts:
- Integration runbook.
- CRM configuration catalogue.
- Deployment validation checklist.
- Known error database.
- Release support checklist.

How to track improvement:
- Mean time to diagnose deployment issues.
- Number of repeat incidents caused by missing documentation.
- Percentage of integrations with current runbooks.
- Percentage of CRM configurations with named owner and last-reviewed date.
- Deployment defects found after release versus during validation.

## 2. System / Architecture Documentation Gaps

Feedback observed:
- Document ITC-owned CRM configuration architecture standards to align with BAT.
- Document ITC-owned integration points and architecture standards to align with BAT.
- Initial brainstorm items included business capability map, architecture principles, decision / assumptions / constraints log, API catalogue / API specifications, and integration architecture diagram.

Research focus:
- Architecture documentation needs to be decision-oriented, not just diagram-oriented.
- The most useful operating set normally includes capability map, context diagram, integration catalogue, API contracts, data ownership, decision log, and non-functional constraints.

Remediation ideas:
- Establish a minimum documentation standard for CRM and integration changes.
- Build a business capability map linked to applications, integrations, and ownership.
- Create and maintain an integration architecture diagram.
- Create an architecture decision record library for major design decisions.
- Align documentation review with BAT architecture governance.

Suggested artefacts:
- Business capability map.
- Integration architecture diagram.
- API catalogue and API specification register.
- Architecture principles.
- Architecture decision record.
- Assumptions and constraints log.
- System ownership matrix.

How to track improvement:
- Percentage of systems/integrations with current architecture documentation.
- Number of delivery decisions captured as ADRs.
- Number of architecture review findings repeated across projects.
- Stakeholder satisfaction score for architecture clarity.
- Time taken for new team members to understand integration landscape.

## 3. Technical Debt Governance

Feedback observed:
- Track ITC technical debt backlog.
- Prioritisation requires BAT product alignment.

Research focus:
- Technical debt is most useful when treated as a managed portfolio rather than a complaint list.
- Strong debt governance captures business impact, operational risk, cost of delay, dependency impact, product alignment, and remediation effort.

Remediation ideas:
- Create a single technical debt backlog in ADO.
- Tag debt items by product, system, risk, effort, and BAT priority.
- Run a monthly debt triage with ITC and BAT product representation.
- Reserve sprint capacity or roadmap allocation for high-risk debt.

Suggested artefacts:
- Technical debt backlog.
- Debt scoring matrix.
- Product alignment register.
- Monthly technical debt review pack.
- Debt burn-down / ageing dashboard.

How to track improvement:
- Count and age of open technical debt items.
- Percentage of debt items with owner, impact, and priority.
- Debt items closed per sprint/month.
- Reduction in incidents linked to known debt.
- Sprint capacity allocated to debt remediation.

## 4. Collaboration Tool Usage - ADO / SharePoint

Feedback observed:
- Improve ticket hygiene and usage practices.

Research focus:
- Tool usage issues often come from unclear working agreements: what belongs in ADO, what belongs in SharePoint, naming standards, required fields, and review discipline.
- Ticket hygiene affects reporting reliability, delivery predictability, and dependency visibility.

Remediation ideas:
- Define minimum ADO ticket standards for epics, features, user stories, defects, and tasks.
- Create examples of good ticket descriptions and acceptance criteria.
- Standardise SharePoint folder structure, naming, versioning, and ownership.
- Run weekly hygiene checks for stale, ownerless, or incomplete tickets.

Suggested artefacts:
- ADO working agreement.
- Ticket quality checklist.
- Epic / feature / user story / defect exemplars.
- SharePoint information architecture.
- Weekly ticket hygiene dashboard.

How to track improvement:
- Percentage of tickets meeting definition of ready.
- Percentage of tickets with owner, priority, due date, acceptance criteria, and current status.
- Number of stale tickets older than agreed threshold.
- Rework caused by unclear tickets.
- SharePoint document duplication or outdated-document count.

## 5. Due Dates and Dependency Tracking

Feedback observed:
- Introduce dashboards and enforce due date tracking.

Research focus:
- Due date tracking needs a governance loop: dates must be visible, challenged, updated, and linked to dependencies and risks.
- Dashboards alone do not improve delivery unless teams agree escalation rules.

Remediation ideas:
- Add mandatory due dates for key delivery items.
- Maintain a dependency tracker with owner, need-by date, impact, and escalation path.
- Create an overdue item dashboard.
- Review overdue and blocked items in weekly delivery governance.

Suggested artefacts:
- Dependency tracker.
- Due date dashboard.
- Blocker and escalation log.
- Milestone tracker.
- Weekly delivery governance pack.

How to track improvement:
- Percentage of active work items with due dates.
- Number of overdue items by age band.
- Average dependency resolution time.
- Percentage of dependencies with owner and need-by date.
- Number of missed milestones caused by unmanaged dependencies.

## 6. Collaboration Tool Usage - Delivery Artefacts

Feedback observed:
- Standardise meeting minutes, actions, and RAID logs.
- Brainstorm included planning artefacts such as stakeholder map, project plan, delivery plan, roadmap, sprint plan, release schedule, milestone tracker, dependency tracker, and resource plan.
- Brainstorm included tracking artefacts such as RAID log, action tracker, decision log, sprint backlog tracker, and delivery status tracker.
- Brainstorm included reporting artefacts such as weekly/monthly status report, RAG status dashboard, KPI tracker, and executive dashboard.

Research focus:
- Delivery artefacts work best as a connected system: decisions create actions, actions change plans, dependencies create RAID entries, and status reporting reflects the underlying evidence.

Remediation ideas:
- Define the mandatory artefact set for ITC delivery.
- Create templates and examples for each artefact.
- Assign named owners and review cadence.
- Store artefacts in one consistent SharePoint/Drive structure.

Suggested artefacts:
- RAID log.
- Action tracker.
- Decision log.
- Delivery plan.
- Milestone tracker.
- Resource plan.
- RAG status dashboard.
- KPI tracker.

How to track improvement:
- Percentage of active initiatives with required artefacts in place.
- Percentage of RAID/action/decision entries reviewed on schedule.
- Number of status reports supported by evidence from trackers.
- Reduction in untracked decisions or orphaned actions.
- Stakeholder confidence score in delivery reporting.

## 7. Sprint Retrospectives and Sprint Reviews

Feedback observed:
- Continue retrospectives and sprint reviews, and track actions.
- Invite six months into the future and enforce attendance and documentation.

Research focus:
- Retrospectives only create improvement when actions are tracked, owned, and revisited.
- Sprint reviews should show completed outcomes and invite stakeholder feedback, not become internal status meetings.

Remediation ideas:
- Schedule recurring sprint ceremonies six months ahead.
- Maintain a retrospective action log.
- Define sprint review evidence expectations.
- Track attendance and action closure.
- Review previous retrospective actions at the start of each retrospective.

Suggested artefacts:
- Sprint retrospective action log.
- Sprint review pack.
- Attendance tracker.
- Continuous improvement backlog.
- Sprint review feedback log.

How to track improvement:
- Retrospective action closure rate.
- Number of repeated retrospective themes.
- Sprint review attendance rate by stakeholder group.
- Percentage of sprint reviews with documented outcomes.
- Stakeholder feedback score after sprint review.

## 8. Communication Clarity

Feedback observed:
- Improve ticket descriptions and meeting summaries.
- Standardise epic, feature, user story, and defect exemplars.

Research focus:
- Communication clarity improves when teams standardise the minimum information needed to make decisions and do work.
- Meeting summaries should capture decisions, actions, owners, dates, and unresolved questions.

Remediation ideas:
- Introduce writing standards for tickets and meeting notes.
- Create exemplars for common ADO work item types.
- Use meeting summary templates with action and decision sections.
- Run quality sampling on tickets and meeting summaries.

Suggested artefacts:
- Ticket description standards.
- Epic / feature / user story / defect examples.
- Meeting minutes template.
- Decision and action capture checklist.
- Quality sampling log.

How to track improvement:
- Percentage of sampled tickets meeting quality standard.
- Number of clarification loops per ticket.
- Action owner/date completeness in meeting notes.
- Defects or rework linked to unclear requirements.
- Stakeholder rating of communication clarity.

## 9. Collaboration Concerns with WE Stakeholders

Feedback observed:
- Align expectations with WE stakeholders.

Research focus:
- Stakeholder collaboration depends on clear roles, governance, escalation routes, and expectation setting.
- Misalignment often appears as late decisions, unclear acceptance, surprise dependencies, and duplicated conversations.

Remediation ideas:
- Create a stakeholder map and engagement plan.
- Agree communication cadence and decision rights with WE stakeholders.
- Document expectation agreements and service boundaries.
- Add stakeholder risks/issues to RAID.

Suggested artefacts:
- Stakeholder map.
- RACI or responsibility matrix.
- Engagement plan.
- Expectation alignment log.
- Escalation pathway.

How to track improvement:
- Number of unresolved stakeholder decisions.
- Stakeholder attendance at agreed governance forums.
- Response time for stakeholder decisions.
- Number of escalations caused by unclear ownership.
- Stakeholder satisfaction pulse score.

## 10. Responsiveness Concerns

Feedback observed:
- Define response expectations with WE market teams.

Research focus:
- Responsiveness improves when teams agree service expectations by request type and priority.
- Response-time targets should separate acknowledgement, triage, update cadence, and resolution.

Remediation ideas:
- Define response SLAs or operating-level agreements by request type.
- Create a shared intake and triage process.
- Publish escalation rules for urgent issues.
- Track acknowledgement and resolution times.

Suggested artefacts:
- Response expectation matrix.
- Intake and triage workflow.
- Escalation matrix.
- Service request dashboard.
- Communications playbook.

How to track improvement:
- Acknowledgement time by priority.
- Triage completion time.
- Resolution time by request type.
- Number of overdue responses.
- Stakeholder satisfaction with responsiveness.

## 11. Meeting Discipline

Feedback observed:
- Standardise meeting minutes, actions, and RAID logs.

Research focus:
- Meeting discipline is less about more meetings and more about consistent purpose, decisions, actions, and follow-through.
- Poor meeting discipline often creates hidden work, unclear accountability, and repeated discussions.

Remediation ideas:
- Require agenda, owner, objective, and expected decisions for recurring meetings.
- Use standard minutes with actions, decisions, risks, and dependencies.
- Review action closure at the start of each meeting.
- Cancel or redesign meetings without clear outputs.

Suggested artefacts:
- Meeting charter.
- Meeting minutes template.
- Action tracker.
- Decision log.
- RAID log.

How to track improvement:
- Percentage of meetings with agenda and minutes.
- Percentage of actions with owner and due date.
- Action closure rate by meeting forum.
- Number of repeated agenda items due to unresolved actions.
- Meeting effectiveness pulse score.

## Cross-Cutting Governance Recommendation

Create a monthly ITC Continuous Improvement Review. Inputs should include:
- RAID log.
- Action tracker.
- Technical debt backlog.
- Dependency tracker.
- Ticket hygiene dashboard.
- Sprint retrospective action log.
- Stakeholder feedback.
- Improvement scorecard.

Outputs should include:
- Decisions made.
- Actions assigned.
- Escalations required.
- Measures improving, stable, or deteriorating.
- Next month focus areas.

