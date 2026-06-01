"""Headless CAD export for the garage shelving model.

Run:
    uv run --with cadquery --python 3.11 python garage_shelving_cadquery.py
"""

from pathlib import Path

import cadquery as cq


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


def part(name, x, y, z, dx, dy, dz):
    solid = cq.Workplane("XY").box(dx, dy, dz)
    return solid.translate((x + dx / 2, y + dy / 2, z + dz / 2)).val().located(cq.Location())


def build():
    assembly = cq.Assembly(name="garage_shelving_metric")

    for idx, z in enumerate(SHELF_Z, 1):
        assembly.add(part(f"rear_2x4_rail_shelf_{idx}", 0, 0, z, LENGTH, TWO_BY_FOUR_W, TWO_BY_FOUR_H), color=cq.Color(0.72, 0.49, 0.25))
        assembly.add(part(f"front_2x4_rail_shelf_{idx}", 0, DEPTH - TWO_BY_FOUR_W, z, LENGTH, TWO_BY_FOUR_W, TWO_BY_FOUR_H), color=cq.Color(0.72, 0.49, 0.25))

        for post_idx, x in enumerate(POST_X, 1):
            assembly.add(part(f"depth_2x4_support_shelf_{idx}_{post_idx}", x, TWO_BY_FOUR_W, z, TWO_BY_FOUR_W, CROSS_SUPPORT, TWO_BY_FOUR_H), color=cq.Color(0.72, 0.49, 0.25))

        deck_z = z + TWO_BY_FOUR_H
        assembly.add(part(f"plywood_96in_shelf_{idx}", 0, 0, deck_z, PANEL_LONG, DEPTH, PLY), color=cq.Color(0.69, 0.58, 0.36))
        assembly.add(part(f"plywood_48in_shelf_{idx}", PANEL_LONG, 0, deck_z, PANEL_SHORT, DEPTH, PLY), color=cq.Color(0.69, 0.58, 0.36))

    for idx, x in enumerate(POST_X, 1):
        assembly.add(part(f"front_upright_2x4_{idx}", x, DEPTH - TWO_BY_FOUR_W, 0, TWO_BY_FOUR_W, TWO_BY_FOUR_W, HEIGHT), color=cq.Color(0.72, 0.49, 0.25))

    return assembly


def main():
    out = Path(__file__).resolve().parent
    model = build()
    model.save(str(out / "garage_shelving_metric.step"))
    model.save(str(out / "garage_shelving_metric.stl"))


if __name__ == "__main__":
    main()
