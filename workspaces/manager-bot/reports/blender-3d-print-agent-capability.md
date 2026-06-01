# Blender 3D Print Agent Capability Report

Date: 2026-05-16
Owner: manager-bot
Status: Initial deployment complete; Blender/admesh/PrusaSlicer validation toolchain installed

## Deployment Update - 2026-05-16

Completed:

- Created Discord channel `#modeling-studio` with ID `1505085743414902819`.
- Added `modeler-bot` workspace at `/home/vin/.openclaw/workspaces/modeler-bot`.
- Added `modeler-bot` to `/home/vin/.openclaw/openclaw.json`.
- Added the new channel to the Discord allowlist and guild channel map.
- Bound `#modeling-studio` to `modeler-bot`.
- Created the local `3d-print-modeling` skill and copied it into the modeler-bot Codex skill path.
- Created Google Drive folder `3D_Models` and child folders `Design_Dev`, `Design_Preproduction`, and `Design_Production`.
- Posted setup notes in `#modeling-studio`.
- Routed toolchain installation to `#admin-desk`.

Validation:

- `openclaw config validate` passes.
- `openclaw agents bindings` shows `modeler-bot <- discord peer=channel:1505085743414902819`.

Completed after unblock request:

- Installed user-local `uv`.
- Created modeler-bot `.venv`.
- Installed `trimesh`, `numpy`, `numpy-stl`, and `networkx`.
- Installed local `admesh` wrapper from extracted Ubuntu packages.
- Installed portable official Blender 5.1.1 in the modeler workspace.
- Installed local PrusaSlicer 2.7.2 CLI from extracted Ubuntu packages.
- Added wrappers: `bin/blender`, `bin/python-mesh`, `bin/admesh`, and `bin/prusa-slicer`.
- Added Neptune 3/4 PLA draft slicer profile at `config/prusaslicer/neptune-3-4-pla-draft.ini`.
- Ran smoke test: `projects/calibration-cube`, version `version_0.1.0`.
- Generated `.blend` and STL.
- Validated STL as watertight with positive volume; admesh reported no holes/disconnected facets/degenerate facets.
- Ran PrusaSlicer dry run against the calibration cube and generated G-code.
- Uploaded smoke-test artifacts to Drive: https://drive.google.com/drive/folders/1BWldOTZqgYgwETl0YTvjJiJFpQLi0ovr

Remaining optional enhancement:

- Tune a production slicer profile against the exact Neptune 3/4 variant, nozzle, and filament brand before using generated G-code for real prints.

## Goal

Add a dedicated Discord channel and agent where Vincent can request printable 3D models. The agent should generate source models, compile/export them through Blender, validate printability, and save artifacts for human review.

The first deployment should produce files only. It should not operate a printer directly.

## Recommendation

Create a new agent named `modeler-bot` and a new Discord channel named `#modeling-studio` or `#3d-print-lab`.

The first version should:

- Accept structured model briefs.
- Generate editable source files, preferably Blender Python plus `.blend`; optionally OpenSCAD/CadQuery later.
- Run Blender headlessly to build and export candidate files.
- Validate geometry before saving review artifacts.
- Save source, exports, previews, and validation reports under the modeler workspace.
- Clearly label outputs as `draft`, `validated for slicer review`, or `blocked`.

Do not add direct printer control in phase one.

## Current System Fit

The current OpenClaw config already follows the right pattern:

- Agents are listed under `/home/vin/.openclaw/openclaw.json`.
- Existing workspaces live under `/home/vin/.openclaw/workspaces/<agent-id>`.
- Discord channel routing uses explicit bindings by channel ID.
- Existing lanes are `manager-bot`, `researcher-bot`, `ops-bot`, and `admin-bot`.

So deployment should be a conventional new-lane addition:

- Add `modeler-bot` to `agents.list`.
- Create `/home/vin/.openclaw/workspaces/modeler-bot`.
- Create the Discord channel.
- Add the new channel ID to the Discord allowlist and guild channel map.
- Add a binding from that channel to `modeler-bot`.

## Proposed Agent Role

`modeler-bot` should own 3D-print modeling tasks.

Role contract:

- Convert user intent into printable model briefs.
- Ask for missing dimensions, printer profile, material, tolerances, and use case when needed.
- Generate or revise editable source models.
- Export STL as the baseline artifact; optionally export 3MF where available.
- Validate units, size, mesh integrity, wall thickness, overhang/support notes, and slicer readiness.
- Preserve assumptions and validation results alongside every output.

Boundaries:

- No direct printer operation initially.
- No unsafe weapon design.
- No claims that load-bearing, medical, food-contact, electrical, heat-exposed, child-safety, or pressure-bearing parts are safe without explicit human review.
- No `ready to print` language unless validation gates pass and assumptions are documented.

## Proposed Workspace Layout

```text
/home/vin/.openclaw/workspaces/modeler-bot/
  AGENTS.md
  SOUL.md
  IDENTITY.md
  TOOLS.md
  HEARTBEAT.md
  projects/
    <project-slug>/
      brief.md
      assumptions.md
      source/
      exports/
      previews/
      validation.md
      iterations.md
```

Source files are the durable artifact. STL/3MF exports are compiled outputs.

## Blender Modeling Requirements

For 3D printing, generated Blender models need to behave like real solids:

- Closed, manifold, watertight geometry.
- Consistent outward normals.
- No self-intersections.
- No zero-area faces or zero-length edges.
- No duplicate internal geometry.
- Dimensions modeled explicitly in millimeters.
- Minimum wall thickness tied to the printer/material/nozzle profile.
- Bounding box checked against target printer build volume.

Relevant Blender capabilities:

- Blender can run headlessly with `blender -b --python script.py`.
- Blender has native STL import/export.
- Blender's 3D Print Toolbox checks volume, surface area, bad geometry, manifold repair, thickness-oriented tools, bed alignment, scaling, and quick STL/PLY/OBJ export.
- Blender Python can inspect mesh topology with `bmesh`, including manifold checks.

## Recommended Generation Workflow

1. Receive or create a structured brief.
2. Generate Blender Python with explicit units and target dimensions.
3. Build geometry from closed primitives/booleans where practical.
4. Apply modifiers before export.
5. Apply scale/rotation intentionally.
6. Recalculate outward normals.
7. Remove duplicate vertices and loose geometry.
8. Save `.blend` and source script.
9. Run validation in headless Blender.
10. Export temporary STL, and optionally 3MF if support is installed.
11. Re-import/export-check in a separate process.
12. Save final artifacts only if validation passes.

Example command shape:

```bash
blender -b --python generate_model.py
blender -b --python validate_and_export.py -- model.blend output.stl
python -m trimesh output.stl
```

## Validation Pipeline

Use multiple validators. No single tool proves physical printability.

Minimum baseline:

- Blender Python preflight.
- STL export.
- `trimesh` validation.
- Slicer dry run with PrusaSlicer using the Neptune 3/4 profile.

Recommended full gate:

- Blender Python checks:
  - exactly one intended printable mesh or documented multi-part assembly
  - units set to metric/millimeters
  - dimensions within printer bounds
  - non-manifold edges count is zero
  - loose geometry count is zero
  - zero-area faces count is zero
  - normals are outward
  - wall thickness is above configured minimum where measurable
- `trimesh`:
  - loadable mesh
  - `is_watertight`
  - positive volume
  - sane extents/bounding box
  - expected component count
- `admesh` for STL-specific diagnostics:
  - normals
  - holes
  - disconnected facets
  - degenerate facets
- Optional `pymeshlab` or MeshLab for cleanup/secondary diagnostics.
- Optional manifold repair only when auto-repair is explicitly allowed.
- PrusaSlicer CLI dry run:
  - confirms a real slicer can process the model with the configured printer/material profile
  - catches many practical slicing failures

Save the model for review only when:

- source and export both exist
- mesh is watertight/manifold
- volume is positive
- dimensions match the brief
- component count matches expectation
- slicer produces non-empty output without fatal errors
- validation report is written

## Toolchain Needed

Initial research found no active installs on PATH/import path for:

- `blender`
- `admesh`
- `trimesh`
- `numpy`
- `numpy-stl`
- `bpy`
- `prusa-slicer`
- `cura`

Install plan for phase one:

- Blender CLI package or official tarball/AppImage.
- Python environment with `trimesh`, `numpy`, and optionally `numpy-stl`.
- `admesh` if available from distro packages.
- PrusaSlicer CLI plus Neptune 3/4 validation profile.
- Optional later: `pymeshlab`, OpenSCAD, CadQuery, Manifold/MeshFix.

## Skill Needed

Create a dedicated skill, likely `3d-print-modeling`.

It should include:

- How to turn a request into a printable model brief.
- Required clarifying questions.
- Blender Python generation conventions.
- Unit/dimension policy.
- Validation checklist.
- Export conventions.
- Project directory layout.
- Safety boundaries.
- Handoff format for manager-bot.
- Examples:
  - calibration cube
  - bracket
  - enclosure
  - simple replacement knob

The skill should prefer parametric, editable source over one-off mesh output.

## Manager Routing

manager-bot should route like this:

- Printable model request: send structured brief to `modeler-bot`.
- Source-heavy design research: ask `researcher-bot` first, then pass findings to `modeler-bot`.
- Package installs or system setup: route to `ops-bot` or `admin-bot` depending on risk.
- Safety-sensitive model: require explicit caveats and human confirmation before calling it validated.

Suggested handoff:

```text
Task:
Use case:
Required dimensions:
Printer/material/nozzle:
Constraints:
References:
Deliverables:
Validation required:
Open questions:
```

## Deployment Steps

1. Choose channel name: `#modeling-studio` or `#3d-print-lab`.
2. Create the Discord channel.
3. Create `modeler-bot` workspace and identity files.
4. Add `modeler-bot` to `openclaw.json`.
5. Add the new channel ID to Discord allowlist/guild channel config.
6. Bind the new channel to `modeler-bot`.
7. Add `3d-print-modeling` skill.
8. Install Blender and minimum validation tools.
9. Run config validation.
10. Smoke test with a harmless 20 mm calibration cube with embossed text.
11. Review saved source/export/validation files.
12. Only then try a real user-requested model.

## Open Questions Before Deployment

Vincent should decide or provide:

- Preferred channel name: `#modeling-studio` or `#3d-print-lab`.
- Target printer model and build volume.
- Preferred material(s), nozzle size, and minimum wall thickness defaults.
- Preferred output format: STL only at first, or STL plus 3MF when possible.
- Whether auto-repair is allowed, and if yes whether repaired models must be separately labeled.
- Where finished artifacts should be stored long term.

## Sources Checked

- Blender 3D Print Toolbox: https://extensions.blender.org/add-ons/print3d-toolbox/
- Blender command line arguments: https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
- Blender STL import/export: https://docs.blender.org/manual/en/latest/files/import_export/stl.html
- Blender bmesh API: https://docs.blender.org/api/current/bmesh.html
- ADMesh CLI: https://admesh.readthedocs.io/en/latest/cli.html
- Slic3r command line reference: https://manual.slic3r.org/advanced/command-line
- trimesh documentation: https://trimesh.org/trimesh.html

## Bottom Line

This capability is feasible. The safest first version is a dedicated `modeler-bot` that creates and validates files, not a printer controller. The core engineering work is installing Blender plus validators, writing the `3d-print-modeling` skill, and enforcing a validation gate before any generated model is saved as ready for human review.
