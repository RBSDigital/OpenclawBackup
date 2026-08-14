---
name: mermaid
description: Compile Mermaid.js diagrams to PNG or SVG images using mmdc.
---

# Mermaid Diagram Compile Skill

This skill allows you to compile Mermaid diagram syntax to images using the `mmdc` command.

## Usage
The `mmdc` command is available in the system PATH.

- **Compile to PNG**:
  ```bash
  mmdc -i input.mmd -o output.png
  ```
- **Compile to SVG**:
  ```bash
  mmdc -i input.mmd -o output.svg
  ```
