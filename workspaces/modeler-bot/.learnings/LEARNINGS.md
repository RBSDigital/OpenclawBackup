# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

---

## [LRN-20260814-001] knowledge_gap

**Logged**: 2026-08-14T13:17:50Z
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
Structurizr CLI is not on the host PATH, but a portable Java 17 runtime plus the official CLI ZIP can still validate and export workspaces locally.

### Details
On this host, `java` is absent and the Docker daemon socket is not accessible to the current user. The workaround that succeeded was downloading a temporary Temurin 17 JRE and the official `structurizr-cli` release ZIP, then running `validate -workspace workspace.dsl` followed by `export -workspace workspace.dsl -format mermaid -output out`.

### Suggested Action
Use a portable Java 17 runtime plus the official CLI ZIP when the host does not have Java installed. Prefer Mermaid export for quick local verification when PNG/SVG browser rendering is not needed.

### Metadata
- Source: conversation
- Related Files: TOOLS.md, scratch/structurizr-learning/workspace.dsl
- Tags: structurizr, c4, dsl, cli, java, mermaid
- Pattern-Key: [REDACTED_SECRET]

---
