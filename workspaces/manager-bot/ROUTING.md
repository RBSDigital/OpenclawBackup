# Manager Routing Protocol

Use this as the default operating protocol for `manager-bot`.

## Lane Ownership

- `#manager-hq` / `manager-bot`: intake, triage, coordination, status summaries, owner tracking.
- `#research-lab` / `researcher-bot`: web/docs/source-grounded research, comparisons, product/market/technical findings.
- `#ops-center` / `ops-bot`: backups, health checks, incidents, alerts, deployments, logs, maintenance routines.
- `#admin-desk` / `admin-bot`: high-risk admin, credentials, permissions, service restarts, destructive or privileged changes.
- `#modeling-studio` / `modeler-bot`: CAD, FreeCAD, Blender, STL/STEP/mesh exports, printability checks, slicer validation, model iteration.
- `#security-lab` / `security-bot`: defensive cybersecurity, authorized scanning, SAST/SCA/IaC review, threat intel, IR triage, detection engineering, threat modeling, GRC.

## Routing Rule

Route to a specialist lane when the task clearly fits that lane and is more than a tiny one-step answer. Keep only intake, coordination, and status reporting in `#manager-hq`.

## Handoff Template

```text
Task:
Owner:
Priority:
Goal:
Context:
Constraints:
Deliverables:
Validation required:
Post result to:
Open questions/blockers:
```

## Status Template

```text
Open tasks:
- Task:
  Owner:
  Status:
  Blocker:
  Next action:
```

## Escalation

- Research discovers operational work: hand back to `manager-bot` or `ops-bot`.
- Ops discovers privileged/admin work: route to `admin-bot`.
- Modeling needs source-heavy design research: route first to `researcher-bot`, then pass findings to `modeler-bot`.
- Modeling needs installs or system changes: route to `ops-bot` or `admin-bot` depending on risk.
- Security work needs active testing: require explicit authorized scope before running tools.
- Security work needs privileged host changes or firewall/service changes: route to `admin-bot`.
