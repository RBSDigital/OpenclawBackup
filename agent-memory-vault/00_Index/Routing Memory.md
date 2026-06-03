# Routing Memory

Primary routing remains defined in `manager-bot` workspace instructions and `ROUTING.md`. This note captures durable cross-agent routing memory for quick recall.

## Lanes

- `manager-bot` / `#manager-hq`: intake, triage, cross-agent status, routing, summaries.
- `researcher-bot` / `#research-lab`: source-heavy web/docs/product/market/technical research.
- `ops-bot` / `#ops-center`: backups, health checks, incidents, alerts, deployments, logs, maintenance.
- `admin-bot` / `#admin-desk`: high-risk admin, credentials, permissions, service restarts, destructive or privileged changes.
- `modeler-bot` / `#modeling-studio`: CAD, FreeCAD, Blender, STL/STEP/mesh exports, slicer validation, 3D-print iteration.
- `security-bot` / `#security-lab`: defensive cybersecurity, authorized scanning, SAST/SCA/IaC, threat intel, IR, detection engineering, GRC.

## Skill Placement Decision

See [[../Decisions/2026-05-30 Agent Skill Assignment]].

## Memory Vault Decision

See [[../Decisions/2026-05-30 Agent Memory Vault Setup]].

## Cost Policy Decision

See [[../Decisions/2026-06-02 API Token Cost Policy]].
