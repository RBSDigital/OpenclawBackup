# Validation Report

- Version: version_0.1.0
- Status: validated-for-review
- STL: /home/vin/.openclaw/workspaces/modeler-bot/projects/calibration-cube/exports/calibration_cube_version_0.1.0.stl
- Watertight: True
- Volume: 8021.265 cubic mm
- Extents: 20.000 x 20.000 x 20.800 mm
- Component count: 5
- Faces: 860
- Vertices: 438
- admesh exit code: 0
- PrusaSlicer dry run: passed
- PrusaSlicer profile: /home/vin/.openclaw/workspaces/modeler-bot/config/prusaslicer/neptune-3-4-pla-draft.ini
- G-code: /home/vin/.openclaw/workspaces/modeler-bot/projects/calibration-cube/slicer/calibration_cube_version_0.1.0_neptune_pla_draft.gcode
- Estimated print time: 21m 19s normal / 22m 3s silent
- Estimated filament: 1440.56 mm / 3.46 cubic cm

## JSON

{
  "file": "/home/vin/.openclaw/workspaces/modeler-bot/projects/calibration-cube/exports/calibration_cube_version_0.1.0.stl",
  "is_watertight": true,
  "volume": 8021.265262078662,
  "bounds_min": [
    -10.0,
    -10.0,
    0.0
  ],
  "bounds_max": [
    10.0,
    10.0,
    20.799999237060547
  ],
  "extents": [
    20.0,
    20.0,
    20.799999237060547
  ],
  "component_count": 5,
  "face_count": 860,
  "vertex_count": 438,
  "admesh_exit_code": 0
}

## admesh

ADMesh version 0.98.5, Copyright (C) 1995, 1996 Anthony D. Martin
ADMesh comes with NO WARRANTY.  This is free software, and you are welcome to
redistribute it under certain conditions.  See the file COPYING for details.
Opening /home/vin/.openclaw/workspaces/modeler-bot/projects/calibration-cube/exports/calibration_cube_version_0.1.0.stl
Checking exact...
All facets connected.  No nearby check necessary.
No unconnected need to be removed.
No holes need to be filled.
Checking normal directions...
Checking normal values...
Calculating volume...
Verifying neighbors...

================= Results produced by ADMesh version 0.98.5 ================
Input file         : /home/vin/.openclaw/workspaces/modeler-bot/projects/calibration-cube/exports/calibration_cube_version_0.1.0.stl
File type          : Binary STL file
Header             : 
============== Size ==============
Min X = -10.000000, Max X =  10.000000
Min Y = -10.000000, Max Y =  10.000000
Min Z =  0.000000, Max Z =  20.799999
========= Facet Status ========== Original ============ Final ====
Number of facets                 :   860                 860
Facets with 1 disconnected edge  :     0                   0
Facets with 2 disconnected edges :     0                   0
Facets with 3 disconnected edges :     0                   0
Total disconnected facets        :     0                   0
=== Processing Statistics ===     ===== Other Statistics =====
Number of parts       :     5        Volume   :  8021.271973
Degenerate facets     :     0
Edges fixed           :     0
Facets removed        :     0
Facets added          :     0
Facets reversed       :     0
Backwards edges       :     0
Normals fixed         :     0

## PrusaSlicer Dry Run

PrusaSlicer 2.7.2 generated G-code successfully using the Neptune 3/4 PLA draft validation profile.

```text
Slicing result exported to /home/vin/.openclaw/workspaces/modeler-bot/projects/calibration-cube/slicer/calibration_cube_version_0.1.0_neptune_pla_draft.gcode
bed_shape = 0x0,225x0,225x225,0x225
max_print_height = 265
nozzle_diameter = 0.4
filament_type = PLA
estimated printing time (normal mode) = 21m 19s
filament used [mm] = 1440.56
filament used [cm3] = 3.46
```
