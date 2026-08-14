---
name: plantuml
description: Compile PlantUML diagram syntax to PNG or SVG images.
---

# PlantUML Compile Skill

This skill allows you to compile PlantUML syntax to images using the `plantuml` command.

## Usage
The `plantuml` command is available in the system PATH and is preconfigured with static Graphviz `dot`.

- **Compile a diagram**:
  ```bash
  plantuml input.puml
  ```
  By default, it outputs a file named `input.png` in the same directory.
- **Compile to SVG**:
  ```bash
  plantuml -tsvg input.puml
  ```
