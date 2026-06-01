// Parametric wall-backed garage shelving model, units in millimeters.

length = 3657.6;
depth = 609.6;
height = 1943.1;
two_by_four_w = 38.1;
two_by_four_h = 88.9;
ply = 12.7;
cross_support = 533.4;
panel_long = 2438.4;
panel_short = 1219.2;
shelf_z = [0, 482.6, 965.2, 1447.8];
post_x = [0, length / 2, length - two_by_four_w];

module board(pos, size, color_value=[0.72, 0.49, 0.25]) {
  color(color_value) translate(pos) cube(size);
}

for (z = shelf_z) {
  board([0, 0, z], [length, two_by_four_w, two_by_four_h]);
  board([0, depth - two_by_four_w, z], [length, two_by_four_w, two_by_four_h]);

  for (x = post_x) {
    board([x, two_by_four_w, z], [two_by_four_w, cross_support, two_by_four_h]);
  }

  board([0, 0, z + two_by_four_h], [panel_long, depth, ply], [0.69, 0.58, 0.36]);
  board([panel_long, 0, z + two_by_four_h], [panel_short, depth, ply], [0.69, 0.58, 0.36]);
}

for (x = post_x) {
  board([x, depth - two_by_four_w, 0], [two_by_four_w, two_by_four_w, height]);
}
