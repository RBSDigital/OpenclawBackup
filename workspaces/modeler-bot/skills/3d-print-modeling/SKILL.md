---
name: 3d-print-modeling
description: Generate, validate, version, and save 3D-printable STL models using Blender-oriented workflows for modeler-bot.
metadata:
  short-description: 3D-print model generation and validation
---

# 3D Print Modeling

Use this skill when a user asks for a 3D-printable model, STL export, Blender model, printable part revision, or validation of a generated mesh.

## Brief First

Before modeling, capture:

- Object/use case.
- Required dimensions in millimeters.
- Fit/tolerance needs.
- Material: PLA, TPU, PETG, ABS, ASA, or Nylon.
- Printer/build volume, default 225 x 225 x 265 mm.
- Whether the part is decorative, fit-check, functional, or safety-sensitive.
- Deliverable version label, default next `version_<major>.<minor>.<patch>`.

Ask concise questions if dimensions, tolerances, or material are missing and a reasonable assumption would risk a bad print.

## Project Layout

Use:

```text
projects/<project-slug>/
  brief.md
  assumptions.md
  source/
  exports/
  previews/
  validation.md
  iterations.md
```

Preserve source. STL is an export, not the only artifact.

## Blender Generation Rules

- Model in millimeters.
- Prefer closed primitives, bevels, booleans, and parametric dimensions.
- Apply modifiers before export.
- Apply or intentionally preserve transforms.
- Recalculate outward normals.
- Remove duplicate vertices and loose geometry.
- Keep the model inside 225 x 225 x 265 mm unless the user explicitly asks for segmented parts.
- Avoid thin walls. If no material-specific threshold is available, use conservative defaults and document them.

## Validation Gate

Do not call an artifact validated unless these are checked and recorded:

- STL exists and can be loaded.
- Units and dimensions match the brief.
- Bounding box fits the Neptune 3/4 build volume.
- Mesh is manifold/watertight.
- Volume is positive.
- Normals are sane.
- Component count matches the expected part count.
- Minimum wall thickness is above the configured/default threshold where measurable.
- Overhang/support needs are documented.
- Source and validation files are saved beside the export.

Preferred automated checks when tools are installed:

- Blender headless: `blender -b --python validate_and_export.py`.
- `trimesh`: watertightness, bounds, volume, component count.
- `admesh`: STL-specific diagnostics.
- PrusaSlicer dry run using `config/prusaslicer/neptune-3-4-pla-draft.ini` for Neptune 3/4 fit and G-code generation checks.

If any required tool is missing, mark validation as partial and list the missing tool.

## Slicer Dry Run

Use the local PrusaSlicer wrapper after mesh validation succeeds:

```bash
/home/vin/.openclaw/workspaces/modeler-bot/bin/prusa-slicer \
  --datadir /home/vin/.openclaw/workspaces/modeler-bot/.local-tools/prusaslicer-datadir \
  --load /home/vin/.openclaw/workspaces/modeler-bot/config/prusaslicer/neptune-3-4-pla-draft.ini \
  --export-gcode \
  --output projects/<project-slug>/slicer/<slug>_<version>_neptune_pla_draft.gcode \
  projects/<project-slug>/exports/<slug>_<version>.stl
```

Record the PrusaSlicer version, profile path, generated G-code path, estimated print time, filament estimate, and any warnings in `validation.md`. Treat this as a dry-run review artifact, not as permission to print without human inspection.

## Versioning

Use labels like `version_2.0.23`.

Auto-repair is allowed only as a separate artifact. Append `_repaired` and record what changed:

- `exports/<slug>_version_2.0.23_repaired.stl`
- `validation.md` entry with before/after dimensions, volume, and repair reason.

Never silently replace the unrepaired export.

## Safety Boundaries

Do not assist unsafe weapon design. Do not claim functional safety for load-bearing, medical, food-contact, electrical, heat-exposed, pressure-bearing, vehicle, or child-safety parts. Mark those as requiring human review and appropriate testing.

## Status Updates

Discord updates should be short:

- what was created
- version label
- validation status: draft, partial, validated-for-review, blocked
- file paths or Drive folder target
- open questions
