difference() {
    scale([0.300, 0.070, 0.150]) {
        cube(1, center=true);
    }
    translate([0, 0.5, -0.075]) {
        rotate([90, 0, 0]) {
            cylinder(h=1.0, r=0.075, $fn=20);
        }
    }
}
