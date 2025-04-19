// ==== PARAMETERS ====
bead_radius = 0.2;
bead_length = 3.0;
bead_spacing = 0.1;  // space between beads

// ==== INPUT: CURVE AS LIST OF 2D POINTS ====
curve_points = [
    [0, 0],
    [0.5, 0],
    [1, 0],
    [1.5, 0],
    [2, 0],
    [2.5,0],
    [3,0]
];

// ==== MODULE: HALF CYLINDER ====
module halfMoon(height, r) {
  translate([r/2,0,-height/2]) difference() {
    cylinder(h=height, r=r, $fn = 64);
    translate([r/2,0,height/2]) cube(size=[r, r*2, height+0.2], center=true);
  }
}

// ==== MODULE: PLACE BEADS ALONG CURVE ====
module place_beads(pts) {
    for (i = [0 : len(pts) - 1]) {
        x = pts[i][0];
        y = pts[i][1];
        z = 0;
        
        translate([x, y, z]) rotate([0,90,90]) halfMoon(3,0.2);
    }
}

// ==== MAIN ====
place_beads(curve_points);