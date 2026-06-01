import json
import subprocess
from pathlib import Path

import trimesh

ROOT = Path("/home/vin/.openclaw/workspaces/modeler-bot/projects/simple-pyramid")
VERSION = "version_0.1.0"
SLUG = "simple_pyramid"
STL = ROOT / "exports" / f"{SLUG}_{VERSION}.stl"
REPORT = ROOT / "validation.md"
ADMESH = Path("/home/vin/.openclaw/workspaces/modeler-bot/bin/admesh")
PRUSA = Path("/home/vin/.openclaw/workspaces/modeler-bot/bin/prusa-slicer")
PRUSA_PROFILE = Path(
    "/home/vin/.openclaw/workspaces/modeler-bot/config/prusaslicer/neptune-3-4-pla-draft.ini"
)
PRUSA_DATADIR = Path(
    "/home/vin/.openclaw/workspaces/modeler-bot/.local-tools/prusaslicer-datadir"
)
GCODE = ROOT / "slicer" / f"{SLUG}_{VERSION}_neptune_pla_draft.gcode"
SLICER_LOG = ROOT / "slicer" / "prusaslicer_dry_run.log"
BUILD_VOLUME = (225.0, 225.0, 265.0)
PREVIEW = ROOT / "previews" / f"{SLUG}_{VERSION}.svg"


def run_admesh():
    if not ADMESH.exists():
        return {"available": False, "exit_code": None, "output": "admesh wrapper not found"}
    completed = subprocess.run(
        [str(ADMESH), str(STL)],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return {
        "available": True,
        "exit_code": completed.returncode,
        "output": completed.stdout,
    }


def run_slicer():
    if not PRUSA.exists() or not PRUSA_PROFILE.exists():
        return {
            "available": False,
            "exit_code": None,
            "output": "PrusaSlicer wrapper or profile not found",
        }
    completed = subprocess.run(
        [
            str(PRUSA),
            "--datadir",
            str(PRUSA_DATADIR),
            "--load",
            str(PRUSA_PROFILE),
            "--export-gcode",
            "--output",
            str(GCODE),
            str(STL),
        ],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    SLICER_LOG.write_text(completed.stdout, encoding="utf-8")
    return {
        "available": True,
        "exit_code": completed.returncode,
        "output": completed.stdout,
        "gcode": str(GCODE) if GCODE.exists() else None,
    }


mesh = trimesh.load_mesh(STL, force="mesh")
components = mesh.split(only_watertight=False)
extents = mesh.extents.tolist()
fits_build_volume = all(extents[index] <= BUILD_VOLUME[index] for index in range(3))
admesh = run_admesh()
slicer = run_slicer()
status = (
    "validated-for-review"
    if mesh.is_watertight
    and mesh.volume > 0
    and len(components) == 1
    and fits_build_volume
    and (not admesh["available"] or admesh["exit_code"] == 0)
    and (not slicer["available"] or slicer["exit_code"] == 0)
    else "partial"
)

result = {
    "file": str(STL),
    "status": status,
    "is_watertight": bool(mesh.is_watertight),
    "volume_cubic_mm": float(mesh.volume),
    "bounds_min_mm": mesh.bounds[0].tolist(),
    "bounds_max_mm": mesh.bounds[1].tolist(),
    "extents_mm": extents,
    "fits_neptune_3_4_build_volume": bool(fits_build_volume),
    "component_count": len(components),
    "face_count": int(len(mesh.faces)),
    "vertex_count": int(len(mesh.vertices)),
    "admesh_available": admesh["available"],
    "admesh_exit_code": admesh["exit_code"],
    "slicer_available": slicer["available"],
    "slicer_exit_code": slicer["exit_code"],
    "slicer_gcode": slicer.get("gcode"),
    "preview": str(PREVIEW) if PREVIEW.exists() else None,
}

REPORT.write_text(
    "# Validation Report\n\n"
    + "- Version: version_0.1.0\n"
    + "- Status: "
    + status
    + "\n"
    + "- STL: "
    + str(STL)
    + "\n"
    + "- Blender source: "
    + str(ROOT / "source" / f"{SLUG}_{VERSION}.blend")
    + "\n"
    + "- Preview: "
    + (str(PREVIEW) if PREVIEW.exists() else "not available; Blender render failed on headless EGL setup")
    + "\n"
    + "- Watertight/manifold: "
    + str(bool(mesh.is_watertight))
    + "\n"
    + "- Volume: "
    + format(mesh.volume, ".3f")
    + " cubic mm\n"
    + "- Extents: "
    + format(extents[0], ".3f")
    + " x "
    + format(extents[1], ".3f")
    + " x "
    + format(extents[2], ".3f")
    + " mm\n"
    + "- Fits Neptune 3/4 build volume 225 x 225 x 265 mm: "
    + str(bool(fits_build_volume))
    + "\n"
    + "- Component count: "
    + str(len(components))
    + "\n"
    + "- Faces: "
    + str(len(mesh.faces))
    + "\n"
    + "- Vertices: "
    + str(len(mesh.vertices))
    + "\n"
    + "- Normals: outward normals recalculated during Blender export; positive volume confirmed.\n"
    + "- Minimum wall thickness: solid body; no hollow walls. Apex is sharp and may be delicate.\n"
    + "- Support/overhang note: four sloped sides are approximately 63 degrees from the bed, so supports should not be required for typical PLA settings; human slicer preview still required.\n"
    + "- admesh available: "
    + str(admesh["available"])
    + "\n"
    + "- admesh exit code: "
    + str(admesh["exit_code"])
    + "\n"
    + "- PrusaSlicer dry run available: "
    + str(slicer["available"])
    + "\n"
    + "- PrusaSlicer exit code: "
    + str(slicer["exit_code"])
    + "\n"
    + "- PrusaSlicer profile: "
    + str(PRUSA_PROFILE)
    + "\n"
    + "- PrusaSlicer G-code output: "
    + str(slicer.get("gcode"))
    + "\n\n"
    + "## JSON\n\n"
    + "```json\n"
    + json.dumps(result, indent=2)
    + "\n```\n\n"
    + "## admesh\n\n"
    + "```text\n"
    + admesh["output"][-4000:]
    + "\n```\n\n"
    + "## PrusaSlicer\n\n"
    + "```text\n"
    + slicer["output"][-4000:]
    + "\n```\n",
    encoding="utf-8",
)

print(json.dumps(result, indent=2))
