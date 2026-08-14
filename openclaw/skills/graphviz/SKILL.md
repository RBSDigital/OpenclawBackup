---
name: graphviz
description: Render Graphviz DOT graphs to PNG or SVG images using dot.
---

# Graphviz Render Skill

This skill allows you to compile Graphviz DOT layout graph syntax to images using the `dot` command.

## Usage
The `dot` command is available in the system PATH.

- **Compile DOT to PNG**:
  ```bash
  dot -Tpng input.dot -o output.png
  ```
- **Compile DOT to SVG**:
  ```bash
  dot -Tsvg input.dot -o output.svg
  ```
