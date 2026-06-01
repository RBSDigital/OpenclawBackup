# Validation Report

- Version: version_0.1.0
- Status: validated-for-review
- STL: /home/vin/.openclaw/workspaces/modeler-bot/projects/simple-pyramid/exports/simple_pyramid_version_0.1.0.stl
- Blender source: /home/vin/.openclaw/workspaces/modeler-bot/projects/simple-pyramid/source/simple_pyramid_version_0.1.0.blend
- Preview: /home/vin/.openclaw/workspaces/modeler-bot/projects/simple-pyramid/previews/simple_pyramid_version_0.1.0.svg
- Watertight/manifold: True
- Volume: 72000.000 cubic mm
- Extents: 60.000 x 60.000 x 60.000 mm
- Fits Neptune 3/4 build volume 225 x 225 x 265 mm: True
- Component count: 1
- Faces: 6
- Vertices: 5
- Normals: outward normals recalculated during Blender export; positive volume confirmed.
- Minimum wall thickness: solid body; no hollow walls. Apex is sharp and may be delicate.
- Support/overhang note: four sloped sides are approximately 63 degrees from the bed, so supports should not be required for typical PLA settings; human slicer preview still required.
- admesh available: True
- admesh exit code: 0
- PrusaSlicer dry run available: True
- PrusaSlicer exit code: 0
- PrusaSlicer profile: /home/vin/.openclaw/workspaces/modeler-bot/config/prusaslicer/neptune-3-4-pla-draft.ini
- PrusaSlicer G-code output: /home/vin/.openclaw/workspaces/modeler-bot/projects/simple-pyramid/slicer/simple_pyramid_version_0.1.0_neptune_pla_draft.gcode
- Google Drive folder: https://drive.google.com/drive/folders/1Dq-iZVUR_zcAeqtQx4Rqst7Ui5bst07G

## JSON

```json
{
  "file": "/home/vin/.openclaw/workspaces/modeler-bot/projects/simple-pyramid/exports/simple_pyramid_version_0.1.0.stl",
  "status": "validated-for-review",
  "is_watertight": true,
  "volume_cubic_mm": 72000.0,
  "bounds_min_mm": [
    -30.0,
    -30.0,
    0.0
  ],
  "bounds_max_mm": [
    30.0,
    30.0,
    60.0
  ],
  "extents_mm": [
    60.0,
    60.0,
    60.0
  ],
  "fits_neptune_3_4_build_volume": true,
  "component_count": 1,
  "face_count": 6,
  "vertex_count": 5,
  "admesh_available": true,
  "admesh_exit_code": 0,
  "slicer_available": true,
  "slicer_exit_code": 0,
  "slicer_gcode": "/home/vin/.openclaw/workspaces/modeler-bot/projects/simple-pyramid/slicer/simple_pyramid_version_0.1.0_neptune_pla_draft.gcode",
  "preview": "/home/vin/.openclaw/workspaces/modeler-bot/projects/simple-pyramid/previews/simple_pyramid_version_0.1.0.svg"
}
```

## admesh

```text
ADMesh version 0.98.5, Copyright (C) 1995, 1996 Anthony D. Martin
ADMesh comes with NO WARRANTY.  This is free software, and you are welcome to
redistribute it under certain conditions.  See the file COPYING for details.
Opening /home/vin/.openclaw/workspaces/modeler-bot/projects/simple-pyramid/exports/simple_pyramid_version_0.1.0.stl
Checking exact...
All facets connected.  No nearby check necessary.
No unconnected need to be removed.
No holes need to be filled.
Checking normal directions...
Checking normal values...
Calculating volume...
Verifying neighbors...

================= Results produced by ADMesh version 0.98.5 ================
Input file         : /home/vin/.openclaw/workspaces/modeler-bot/projects/simple-pyramid/exports/simple_pyramid_version_0.1.0.stl
File type          : Binary STL file
Header             : 
============== Size ==============
Min X = -30.000000, Max X =  30.000000
Min Y = -30.000000, Max Y =  30.000000
Min Z =  0.000000, Max Z =  60.000000
========= Facet Status ========== Original ============ Final ====
Number of facets                 :     6                   6
Facets with 1 disconnected edge  :     0                   0
Facets with 2 disconnected edges :     0                   0
Facets with 3 disconnected edges :     0                   0
Total disconnected facets        :     0                   0
=== Processing Statistics ===     ===== Other Statistics =====
Number of parts       :     1        Volume   :  71999.992188
Degenerate facets     :     0
Edges fixed           :     0
Facets removed        :     0
Facets added          :     0
Facets reversed       :     0
Backwards edges       :     0
Normals fixed         :     0

```

## PrusaSlicer

```text
10 => Processing triangulated mesh
20 => Generating perimeters
30 => Preparing infill
45 => Making infill
65 => Searching support spots
69 => Alert if supports needed
89 => Calculating overhanging perimeters
88 => Generating skirt and brim
90 => Exporting G-code to /home/vin/.openclaw/workspaces/modeler-bot/projects/simple-pyramid/slicer/simple_pyramid_version_0.1.0_neptune_pla_draft.gcode
Slicing result exported to /home/vin/.openclaw/workspaces/modeler-bot/projects/simple-pyramid/slicer/simple_pyramid_version_0.1.0_neptune_pla_draft.gcode

```
