---
name: structurizr
description: Create software architecture diagrams using Structurizr C4 DSL.
---

# Structurizr Skill

This skill allows you to write, validate, and export software architecture diagrams using the Structurizr DSL and CLI.

## Tool Availability
The Structurizr CLI is installed and globally available in the system PATH as `structurizr`.

## Structurizr DSL Structure
A Structurizr DSL file defines a workspace containing a software architecture model and views. Here is a basic template:

```structurizr
workspace {
    model {
        user = person "User" "A user of the system."
        softwareSystem = softwareSystem "Software System" "My software system."
        user -> softwareSystem "Uses"
    }
    views {
        systemContext softwareSystem "SystemContext" {
            include *
            autolayout lr
        }
        theme default
    }
}
```

## Available Commands

1. **Validate and Inspect Workspace**:
   Check a workspace DSL file for any errors or architectural design alerts:
   ```bash
   structurizr inspect -w workspace.dsl
   ```

2. **Export Diagrams**:
   Export views to different formats like Mermaid, PlantUML, or JSON:
   ```bash
   # Export to Mermaid format (recommended for rendering)
   structurizr export -w workspace.dsl -f mermaid

   # Export to PlantUML format
   structurizr export -w workspace.dsl -f plantuml
   ```

3. **Push to Structurizr Service (Cloud/On-Premises)**:
   Publish the workspace diagram to a Structurizr server instance:
   ```bash
   structurizr push -w workspace.dsl -id <workspaceId> -key <apiKey> -secret <apiSecret>
   ```
