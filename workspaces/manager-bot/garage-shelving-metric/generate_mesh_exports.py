"""Generate simple mesh/viewer exports without external CAD dependencies."""

from pathlib import Path


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


def boxes():
    items = []
    for shelf, z in enumerate(SHELF_Z, 1):
        items.append((f"rear_2x4_rail_shelf_{shelf}", 0, 0, z, LENGTH, TWO_BY_FOUR_W, TWO_BY_FOUR_H))
        items.append((f"front_2x4_rail_shelf_{shelf}", 0, DEPTH - TWO_BY_FOUR_W, z, LENGTH, TWO_BY_FOUR_W, TWO_BY_FOUR_H))
        for idx, x in enumerate(POST_X, 1):
            items.append((f"depth_2x4_support_shelf_{shelf}_{idx}", x, TWO_BY_FOUR_W, z, TWO_BY_FOUR_W, CROSS_SUPPORT, TWO_BY_FOUR_H))
        deck_z = z + TWO_BY_FOUR_H
        items.append((f"plywood_96in_shelf_{shelf}", 0, 0, deck_z, PANEL_LONG, DEPTH, PLY))
        items.append((f"plywood_48in_shelf_{shelf}", PANEL_LONG, 0, deck_z, PANEL_SHORT, DEPTH, PLY))
    for idx, x in enumerate(POST_X, 1):
        items.append((f"front_upright_2x4_{idx}", x, DEPTH - TWO_BY_FOUR_W, 0, TWO_BY_FOUR_W, TWO_BY_FOUR_W, HEIGHT))
    return items


def vertices(x, y, z, dx, dy, dz):
    return [
        (x, y, z), (x + dx, y, z), (x + dx, y + dy, z), (x, y + dy, z),
        (x, y, z + dz), (x + dx, y, z + dz), (x + dx, y + dy, z + dz), (x, y + dy, z + dz),
    ]


FACES = [
    (1, 2, 3, 4), (5, 8, 7, 6), (1, 5, 6, 2),
    (2, 6, 7, 3), (3, 7, 8, 4), (4, 8, 5, 1),
]

TRIS = [
    (0, 1, 2), (0, 2, 3), (4, 7, 6), (4, 6, 5), (0, 4, 5), (0, 5, 1),
    (1, 5, 6), (1, 6, 2), (2, 6, 7), (2, 7, 3), (3, 7, 4), (3, 4, 0),
]


def write_obj(out, items):
    lines = ["# garage shelving metric OBJ"]
    offset = 0
    for name, x, y, z, dx, dy, dz in items:
        lines.append(f"o {name}")
        for vx, vy, vz in vertices(x, y, z, dx, dy, dz):
            lines.append(f"v {vx:.3f} {vy:.3f} {vz:.3f}")
        for face in FACES:
            lines.append("f " + " ".join(str(offset + i) for i in face))
        offset += 8
    out.write_text("\n".join(lines) + "\n")


def normal(a, b, c):
    ux, uy, uz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
    vx, vy, vz = c[0] - a[0], c[1] - a[1], c[2] - a[2]
    nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
    mag = (nx * nx + ny * ny + nz * nz) ** 0.5 or 1
    return nx / mag, ny / mag, nz / mag


def write_stl(out, items):
    lines = ["solid garage_shelving_metric"]
    for name, x, y, z, dx, dy, dz in items:
        verts = vertices(x, y, z, dx, dy, dz)
        for tri in TRIS:
            pts = [verts[i] for i in tri]
            n = normal(*pts)
            lines.append(f"  facet normal {n[0]:.6g} {n[1]:.6g} {n[2]:.6g}")
            lines.append("    outer loop")
            for p in pts:
                lines.append(f"      vertex {p[0]:.3f} {p[1]:.3f} {p[2]:.3f}")
            lines.append("    endloop")
            lines.append("  endfacet")
    lines.append("endsolid garage_shelving_metric")
    out.write_text("\n".join(lines) + "\n")


def write_svg(out):
    scale = 0.08
    width = LENGTH * scale + 160
    height = 330
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height}" viewBox="0 0 {width:.0f} {height}">',
        '<rect width="100%" height="100%" fill="#f6f3ee"/>',
        '<style>text{font-family:Arial,sans-serif;font-size:13px;fill:#333}.dim{stroke:#333;stroke-width:1;marker-start:url(#a);marker-end:url(#a)}.wood{fill:#b88a4b;stroke:#5f421f}.ply{fill:#c6a56a;stroke:#5f421f}</style>',
        '<defs><marker id="a" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#333"/></marker></defs>',
    ]
    x0, y0 = 70, 80
    for idx, z in enumerate(SHELF_Z):
        y = y0 + idx * 45
        lines.append(f'<rect class="ply" x="{x0}" y="{y - 12}" width="{LENGTH * scale:.1f}" height="16"/>')
        lines.append(f'<rect class="wood" x="{x0}" y="{y}" width="{LENGTH * scale:.1f}" height="8"/>')
    for x in POST_X:
        sx = x0 + x * scale
        lines.append(f'<rect class="wood" x="{sx:.1f}" y="{y0 - 16}" width="{TWO_BY_FOUR_W * scale:.1f}" height="{HEIGHT * scale:.1f}"/>')
    lines.append(f'<line class="dim" x1="{x0}" y1="35" x2="{x0 + LENGTH * scale:.1f}" y2="35"/>')
    lines.append(f'<text x="{x0 + LENGTH * scale / 2 - 45:.1f}" y="28">3657.6 mm / 144 in</text>')
    lines.append(f'<line class="dim" x1="{x0 + LENGTH * scale + 45:.1f}" y1="{y0 - 16}" x2="{x0 + LENGTH * scale + 45:.1f}" y2="{y0 - 16 + HEIGHT * scale:.1f}"/>')
    lines.append(f'<text x="{x0 + LENGTH * scale + 52:.1f}" y="{y0 + HEIGHT * scale / 2:.1f}">1943.1 mm</text>')
    lines.append('<text x="70" y="300">Depth: 609.6 mm / 24 in. Shelf spacing shown: 482.6 mm / 19 in.</text>')
    lines.append("</svg>")
    out.write_text("\n".join(lines) + "\n")


def main():
    out = Path(__file__).resolve().parent
    items = boxes()
    write_obj(out / "garage_shelving_metric.obj", items)
    write_stl(out / "garage_shelving_metric_ascii.stl", items)
    write_svg(out / "garage_shelving_metric_dimensions.svg")


if __name__ == "__main__":
    main()
