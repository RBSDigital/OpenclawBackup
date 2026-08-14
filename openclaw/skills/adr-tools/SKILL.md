---
name: adr-tools
description: Manage Architecture Decision Records (ADRs) using standardized templates.
---

# Architectural Decision Records (ADR) Skill

This skill allows you to initialize, document, list, and link Architectural Decision Records (ADRs) under the project workspace.

## Usage
The `adr-tools` commands are available in the system PATH.

- **Initialize ADR repository**:
  ```bash
  adr init doc/architecture/decisions
  ```
- **Create a new ADR**:
  ```bash
  adr new "Title of the Decision"
  ```
  This creates a markdown template (e.g. `doc/architecture/decisions/0001-title-of-the-decision.md`).
- **List existing ADRs**:
  ```bash
  adr list
  ```
- **Link dependent ADRs**:
  Link a new ADR as superceding or replacing an existing one:
  ```bash
  adr new -s 1 "Use PostgreSQL instead of MySQL"
  ```
