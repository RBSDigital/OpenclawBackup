import json
import subprocess
from pathlib import Path

import trimesh

ROOT = Path("/home/vin/.openclaw/workspaces/modeler-bot/projects/calibration-cube")
STL = ROOT / "exports/calibration_cube_version_0.1.0.stl"
REPORT = ROOT / "validation.md"
ADMESH = Path("/home/vin/.openclaw/workspaces/modeler-bot/bin/admesh")

mesh = trimesh.load_mesh(STL, force="mesh")
components = mesh.split(only_watertight=False)

admesh = subprocess.run(
    [str(ADMESH), str(STL)],
    check=False,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)

result = {
    "file": str(STL),
    "is_watertight": bool(mesh.is_watertight),
    "volume": float(mesh.volume),
    "bounds_min": mesh.bounds[0].tolist(),
    "bounds_max": mesh.bounds[1].tolist(),
    "extents": mesh.extents.tolist(),
    "component_count": len(components),
    "face_count": int(len(mesh.faces)),
    "vertex_count": int(len(mesh.vertices)),
    "admesh_exit_code": admesh.returncode,
}

status = "validated-for-review" if result["is_watertight"] and result["volume"] > 0 else "partial"

REPORT.write_text(
    "# Validation Report\n\n"
    + "- Version: version_0.1.0\n"
    + "- Status: " + status + "\n"
    + "- STL: " + str(STL) + "\n"
    + "- Watertight: " + str(result["is_watertight"]) + "\n"
    + "- Volume: " + format(result["volume"], ".3f") + " cubic mm\n"
    + "- Extents: "
    + format(result["extents"][0], ".3f") + " x "
    + format(result["extents"][1], ".3f") + " x "
    + format(result["extents"][2], ".3f") + " mm\n"
    + "- Component count: " + str(result["component_count"]) + "\n"
    + "- Faces: " + str(result["face_count"]) + "\n"
    + "- Vertices: " + str(result["vertex_count"]) + "\n"
    + "- admesh exit code: " + str(result["admesh_exit_code"]) + "\n\n"
    + "## JSON\n\n"
    + json.dumps(result, indent=2)
    + "\n\n"
    + "## admesh\n\n"
    + admesh.stdout[-4000:]
    + "\n",
    encoding="utf-8",
)

print(json.dumps({"status": status, **result}, indent=2))

