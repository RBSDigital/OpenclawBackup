# TOOLS.md - Local Notes

## Printer Profile

- Printer family: Elegoo Neptune 3/4.
- Build volume: 225 x 225 x 265 mm.
- Bed leveling: 121 points / 11 x 11 auto bed leveling.
- Supported materials: PLA, TPU, PETG, ABS, ASA, Nylon.
- Output policy: STL only first.

## Artifact Storage

Long-term destination: Google Drive `3D_Models`.

Child folders:
- `Design_Dev` - drafts, experiments, early generated outputs.
- `Design_Preproduction` - validated candidate models awaiting final acceptance.
- `Design_Production` - accepted final models.

Standing policy:
- Save every created model project to Google Drive under the appropriate `3D_Models` child folder.
- Use `Design_Dev` for drafts and experiments.
- Use `Design_Preproduction` for validated-for-review candidates.
- Use `Design_Production` only for human-accepted final models.
- Preserve the same core artifact set in Drive when available: STL export, editable source, brief, assumptions, validation report, iterations, previews, and generation/validation scripts.

Folder IDs:
- `3D_Models`: `1586kS_xBX9KXmeSO3wIJZ6OnTgbzd9jK`
- `Design_Dev`: `1BcqZJ-t9CKzYMrJD2camw0lnHVw-EbMc`
- `Design_Preproduction`: `1TpVVnzEzNdsP1qRtmYmQLnjqxXoUEgtj`
- `Design_Production`: `1BeVxp3eKeeySzUg2tLFYgNQufTbMiONT`

Folder URLs:
- `3D_Models`: https://drive.google.com/drive/folders/1586kS_xBX9KXmeSO3wIJZ6OnTgbzd9jK
- `Design_Dev`: https://drive.google.com/drive/folders/1BcqZJ-t9CKzYMrJD2camw0lnHVw-EbMc
- `Design_Preproduction`: https://drive.google.com/drive/folders/1TpVVnzEzNdsP1qRtmYmQLnjqxXoUEgtj
- `Design_Production`: https://drive.google.com/drive/folders/1BeVxp3eKeeySzUg2tLFYgNQufTbMiONT

## Versioning

Use labels like `version_2.0.23`.

If a mesh is automatically repaired, save it as a separate labeled artifact, for example:
- `version_2.0.23_repaired.stl`
- `version_2.0.23_repaired_validation.md`

Never overwrite a prior accepted export.

## Toolchain Status

Toolchain status after 2026-05-16 unblock:

- Python mesh validation: available at `.venv/bin/python`.
- Installed Python packages: `trimesh`, `numpy`, `numpy-stl`, `networkx`.
- Convenience wrapper: `bin/python-mesh`.
- `admesh`: available through local extracted package wrapper `bin/admesh`.
- `blender`: available through portable official Blender 5.1.1 wrapper `bin/blender`.
- `prusa-slicer`: pending install/profile.
- `cura`: not used for phase one.

Full local file-generation validation can use `bin/blender`, `bin/python-mesh`, and `bin/admesh`.

## Smoke Test

Completed 2026-05-16:

- Project: `projects/calibration-cube`
- Version: `version_0.1.0`
- Blender: generated `.blend` and STL with portable Blender 5.1.1.
- Python mesh validation: passed, watertight true, positive volume.
- admesh: passed, no holes/disconnected facets/degenerate facets.
- Note: embossed label created multiple shells/components; acceptable for smoke test, but production models should prefer single-body output unless multi-shell is intentional.
- Drive folder: https://drive.google.com/drive/folders/1BWldOTZqgYgwETl0YTvjJiJFpQLi0ovr

## Shared Agent Memory Vault

- Path: `/home/vin/ObsidianVaults/AdaKTVault/06_system/agent-memory-vault`
- Primary folders: `Modeling/`, `Decisions/`
- Promote reusable printer defaults, toolchain lessons, and validation patterns only.
- Keep project artifacts in this workspace and Drive unless a sanitized durable lesson belongs in shared memory.
