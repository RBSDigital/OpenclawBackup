# Garage Shelving Metric Model Package

Project: wall-backed garage shelving similar to the reference image.

Primary dimensions:
- Overall length: 144 in = 3657.6 mm
- Shelf depth: 24 in = 609.6 mm
- Nominal height from cut list uprights: 76.5 in = 1943.1 mm
- Shelf bay spacing shown in reference: 19 in = 482.6 mm
- 2x4 modeled as actual lumber size: 1.5 x 3.5 in = 38.1 x 88.9 mm
- 1/2 in sheet goods modeled as: 12.7 mm

Cut list converted to metric:
- 8 x 2x4 @ 12 ft = 3657.6 mm
- 3 x 2x4 @ 76.5 in = 1943.1 mm
- 12 x 2x4 @ 21 in = 533.4 mm
- 4 x 1/2 in plywood/OSB @ 24 x 96 in = 609.6 x 2438.4 mm
- 4 x 1/2 in plywood/OSB @ 24 x 48 in = 609.6 x 1219.2 mm

Materials converted to metric:
- 2x4 @ 12 ft = 3657.6 mm
- 2x4 @ 8 ft = 2438.4 mm
- 92-5/8 in stud = 2352.7 mm
- 3 in screws = 76.2 mm, about 150
- 2 in screws = 50.8 mm, about 100

Files:
- `garage_shelving_metric.FCStd`: native FreeCAD document generated with FreeCAD 1.1.1.
- `garage_shelving_metric.step`: STEP export for other CAD tools.
- `garage_shelving_metric.brep`: OpenCascade BREP export.
- `garage_shelving_metric.obj` and `garage_shelving_metric_ascii.stl`: mesh imports.
- `garage_shelving_metric_dimensions.svg`: simple dimension sheet.
- `garage_shelving_freecad.py`: FreeCAD Python script to generate the model in FreeCAD and export it.
- `garage_shelving_cadquery.py`: headless CadQuery generator for STEP/STL exports.
- `garage_shelving.scad`: OpenSCAD-style parametric source.
- `garage_shelving_cut_list_metric.csv`: metric cut list.

Notes:
- The source cut list has only 3 uprights at 76.5 in, so this model assumes the rear is wall-supported and the 3 uprights are the front posts, matching common garage-shelf plans.
- The reference image text says 6 ft tall, while the cut list uses 76.5 in / 1943.1 mm. The model follows the cut list.
