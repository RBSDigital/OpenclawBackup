# Toolchain Bootstrap

Status: unblocked for phase-one local generation and validation

The modeler workspace and routing are configured. Python mesh validation, local `admesh`, portable Blender 5.1.1, and local PrusaSlicer CLI are available.

## Completed Without Sudo

`python3.12-venv` could not be installed without sudo, so the workspace uses user-local `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
cd /home/vin/.openclaw/workspaces/modeler-bot
uv venv --python python3 .venv
uv pip install --python .venv/bin/python trimesh numpy numpy-stl networkx
```

`admesh` was installed locally by downloading/extracting Ubuntu packages into `.local-tools/admesh`.

Use:

```bash
/home/vin/.openclaw/workspaces/modeler-bot/bin/python-mesh
/home/vin/.openclaw/workspaces/modeler-bot/bin/admesh
/home/vin/.openclaw/workspaces/modeler-bot/bin/blender
/home/vin/.openclaw/workspaces/modeler-bot/bin/prusa-slicer
```

Portable Blender was installed from the official Blender 5.1.1 Linux x64 tarball into `.local-tools/blender-official`.

PrusaSlicer 2.7.2 was installed locally by downloading/extracting Ubuntu packages into `.local-tools/prusa-slicer`.

Validation profile:

- `config/prusaslicer/neptune-3-4-pla-draft.ini`
- Build volume: 225 x 225 x 265 mm
- Default dry-run material: PLA, 1.75 mm, 0.4 mm nozzle
- Firmware flavor: Marlin
- Start G-code includes `G29` for auto bed leveling

## Required System Packages

Optional system install alternative:

```bash
sudo apt install blender
```

PrusaSlicer can alternatively be installed system-wide later:

```bash
sudo apt install prusa-slicer
```

## Python Validation Environment

If the system `python3.12-venv` package is later installed, the venv can be recreated with:

```bash
cd /home/vin/.openclaw/workspaces/modeler-bot
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install trimesh numpy numpy-stl
```

## Verification

```bash
command -v blender
/home/vin/.openclaw/workspaces/modeler-bot/bin/admesh --version
/home/vin/.openclaw/workspaces/modeler-bot/bin/prusa-slicer --help
.venv/bin/python - <<'PY'
import trimesh, numpy, stl
print('mesh validation imports ok')
PY
```

Generated models can now use local Blender validation through `bin/blender` and slicer dry runs through `bin/prusa-slicer`.

## Smoke Test Result

Completed `projects/calibration-cube`:

- STL: `exports/calibration_cube_version_0.1.0.stl`
- Blend: `source/calibration_cube_version_0.1.0.blend`
- Validation: `validation.md`
- Status: `validated-for-review`
- Drive folder: https://drive.google.com/drive/folders/1BWldOTZqgYgwETl0YTvjJiJFpQLi0ovr
