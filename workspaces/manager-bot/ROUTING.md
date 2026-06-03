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

Use `COST_POLICY.md` before routing work that may require multiple model calls, long context, detached sessions, or specialist agents. Assign one owner, pass only bounded context, and prefer exact files/links over raw conversation history.

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
Token/cost guardrails:
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

## Cost Controls

- Use deterministic tools first for inspection, search, status checks, and mechanical transformations.
- Keep specialist handoffs concise and bounded to the task.
- Do not spawn duplicate agents against the same source material unless an explicit second opinion is needed.
- Escalate to high-reasoning models only for complex judgment, risky changes, or deep synthesis.
- Capture reusable decisions in the shared Agent Memory Vault.
