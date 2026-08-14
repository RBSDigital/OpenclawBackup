---
name: schemacrawler
description: Reverse-engineer database schemas and generate ER diagrams using SchemaCrawler.
---

# SchemaCrawler Database Modeling Skill

This skill allows you to inspect database schemas and output visual ER diagrams or schema definitions using the `schemacrawler` command.

## Usage
The `schemacrawler` command is available in the system PATH.

- **Command Syntax**:
  ```bash
  schemacrawler --server=<db-type> --host=<host> --port=<port> --database=<dbname> --user=<user> --password=[REDACTED_SECRET] --command=<command>
  ```
  Commands include `schema` (output text schema representation), `diagram` (output graphical schema using Graphviz `dot`), etc.
