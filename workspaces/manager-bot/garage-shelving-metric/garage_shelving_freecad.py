"""FreeCAD generator for wall-backed garage shelving.

Run in FreeCAD:
    FreeCADCmd garage_shelving_freecad.py

This creates a document and attempts to save/export beside the script.
"""

from pathlib import Path

import FreeCAD as App
import Part


MM_PER_IN = 25.4
LENGTH = 144 * MM_PER_IN
DEPTH = 24 * MM_PER_IN
HEIGHT = 76.5 * MM_PER_IN
TWO_BY_FOUR_W = 1.5 * MM_PER_IN
TWO_BY_FOUR_H = 3.5 * MM_PER_IN
PLY = 0.5 * MM_PER_IN
CROSS_SUPPORT = 21 * MM_PER_IN
PANEL_LONG = 96 * MM_PER_IN
PANEL_SHORT = 48 * MM_PER_IN

SHELF_Z = [0, 19 * MM_PER_IN, 38 * MM_PER_IN, 57 * MM_PER_IN]
POST_X = [0, LENGTH / 2, LENGTH - TWO_BY_FOUR_W]


def box(doc, name, x, y, z, dx, dy, dz, color):
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = Part.makeBox(dx, dy, dz, App.Vector(x, y, z))
    if getattr(obj, "ViewObject", None):
        obj.ViewObject.ShapeColor = color
    return obj


def main():
    doc = App.newDocument("garage_shelving_metric")

    lumber = (0.72, 0.49, 0.25)
    sheet = (0.69, 0.58, 0.36)
    wall = (0.82, 0.82, 0.80)

    box(doc, "wall_reference", -50, -30, 0, LENGTH + 100, 20, HEIGHT + 150, wall)

    for z in SHELF_Z:
        rail_z = z
        box(doc, "rear_2x4_rail", 0, 0, rail_z, LENGTH, TWO_BY_FOUR_W, TWO_BY_FOUR_H, lumber)
        box(doc, "front_2x4_rail", 0, DEPTH - TWO_BY_FOUR_W, rail_z, LENGTH, TWO_BY_FOUR_W, TWO_BY_FOUR_H, lumber)

        for x in POST_X:
            box(doc, "depth_2x4_support", x, TWO_BY_FOUR_W, rail_z, TWO_BY_FOUR_W, CROSS_SUPPORT, TWO_BY_FOUR_H, lumber)

        deck_z = rail_z + TWO_BY_FOUR_H
        box(doc, "plywood_panel_96in", 0, 0, deck_z, PANEL_LONG, DEPTH, PLY, sheet)
        box(doc, "plywood_panel_48in", PANEL_LONG, 0, deck_z, PANEL_SHORT, DEPTH, PLY, sheet)

    for x in POST_X:
        box(doc, "front_upright_2x4", x, DEPTH - TWO_BY_FOUR_W, 0, TWO_BY_FOUR_W, TWO_BY_FOUR_W, HEIGHT, lumber)

    doc.recompute()
    out = Path(__file__).resolve().parent
    doc.saveAs(str(out / "garage_shelving_metric.FCStd"))
    Part.export(doc.Objects, str(out / "garage_shelving_metric.step"))
    Part.export(doc.Objects, str(out / "garage_shelving_metric.brep"))


if __name__ == "__main__":
    main()
