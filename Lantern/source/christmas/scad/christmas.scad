// Christmas lithophane panels — original relief art.
// Four parts: tree, snowman, reindeer, wreath.
// Size comes from panel_lib.scad: 77.5 x 105 x 1.8 mm.
// The shipped tree and wreath STLs are frozen. The shipped snowman and
// reindeer STLs are the v6 meshes from tools/build_v6_panels.py, traced
// from the approved images. Do not overwrite them from this file.
// Graphics approved 9 Nov 2026, 1:23 PM ET. The 77.5 × 105 × 1.8 mm panels have been printed and fit the lantern well (confirmed by Shannon, Nov 2026).

include <panel_lib.scad>

part = "tree"; // tree | snowman | reindeer | wreath | blank

// ---------------------------------------------------------------------------
// Tree: tiered silhouette, star, round ornaments, short garland.
// ---------------------------------------------------------------------------
module tree_tier(base_y, peak_y, half_w) {
    hull() {
        translate([0, peak_y]) circle(d=6.6, $fn=28);
        translate([-half_w, base_y]) circle(d=9, $fn=24);
        translate([ half_w, base_y]) circle(d=9, $fn=24);
    }
    for (t = [0.36, 0.68]) {
        x = half_w * (1 - t);
        y = base_y + (peak_y - base_y) * t;
        translate([-x - 1.5, y]) circle(d=6.2, $fn=16);
        translate([ x + 1.5, y]) circle(d=6.2, $fn=16);
    }
}

module tree_trunk() {
    translate([0, -37]) offset(r=2) square([8, 12], center=true);
}

module star_2d(r=9.6, inner=0.5) {
    pts = [for (i = [0:9])
        let(a = i*36 + 90, rad = (i % 2 == 0) ? r : r*inner)
        [rad*cos(a), rad*sin(a)]];
    offset(r=1.3) offset(delta=-1.3) polygon(pts);
}

module tree_body_2d() {
    front_of(1.55) {
        union() {
            tree_trunk();
            tree_tier(-34, -7, 26);
            tree_tier(-17, 11, 18.2);
            tree_tier(1, 27, 11.2);
        }
        translate([0, 35.2]) star_2d(9.5, 0.50);
    }
}

module tree_grooves_2d() {
    translate([-12, -26]) circle(d=8.2, $fn=28);
    translate([11, -23.5]) circle(d=7.6, $fn=28);
    translate([0, -15.5]) circle(d=7.4, $fn=28);
    translate([-7.5, -1.5]) circle(d=7.2, $fn=26);
    translate([7.2, 3]) circle(d=6.8, $fn=26);
    translate([0, 15]) circle(d=6.4, $fn=24);
    seg2d([-14, -27], [-4, -21], 1.75);
    seg2d([-4, -21], [5, -27], 1.75);
    seg2d([5, -27], [14, -21], 1.75);
    seg2d([-9, -3], [0, 3.5], 1.7);
    seg2d([0, 3.5], [9, -1.5], 1.7);
    translate([0, 35.2]) circle(d=4.0, $fn=20);
}

// ---------------------------------------------------------------------------
// Reindeer: side-view head, neck, ear, muzzle and branched antlers.
// Original relief. Proportions inspired by public photographs, not traced.
// ---------------------------------------------------------------------------
module rein_head() {
    translate([6, -2]) scale([1.08, 0.86]) circle(d=32, $fn=48);
}
module rein_muzzle() {
    hull() {
        translate([-4, -5]) circle(d=14, $fn=28);
        translate([-16, -8]) circle(d=10, $fn=24);
    }
    translate([-23, -9]) circle(d=11, $fn=28);
}
module rein_ear() {
    hull() {
        translate([13, 4]) circle(d=6.5, $fn=16);
        translate([18, 20]) circle(d=3.2, $fn=12);
    }
    hull() {
        translate([13, 4]) circle(d=6.5, $fn=16);
        translate([24, 12]) circle(d=3.2, $fn=12);
    }
}
module rein_neck() {
    hull() {
        translate([10, -16]) circle(d=18, $fn=28);
        translate([12, -36]) circle(d=18, $fn=28);
    }
}
function qbez(a, b, c, t) = (1-t)*(1-t)*a + 2*(1-t)*t*b + t*t*c;
module taper_curve(a, b, c, w0, w1, n=14) {
    for (i = [0:n-1]) {
        t0 = i / n;
        seg2d(qbez(a, b, c, t0), qbez(a, b, c, t0 + 1/n), w0 + (w1-w0)*t0);
    }
}
module rein_antlers() {
    // Main beam bows backward, then the tip returns upward.
    taper_curve([9, 10], [20, 22], [8, 36], 5.8, 3.6, 18);
    // Two short crown points, split from the top of the beam.
    taper_curve([8, 34], [3, 39], [1, 43], 3.3, 2.4, 7);
    taper_curve([11, 33], [16, 38], [17, 43], 3.3, 2.4, 7);
    // Brow tine, a short curve over the forehead.
    taper_curve([8, 13], [0, 17], [-8, 15], 3.8, 2.5, 8);
    // One short mid tine, not a second beam.
    taper_curve([15, 22], [11, 26], [9, 30], 3.4, 2.4, 6);
}
module reindeer_body_2d() {
    union() {
        rein_neck();
        rein_head();
        rein_muzzle();
        rein_ear();
        rein_antlers();
    }
}
module reindeer_grooves_2d() {
    translate([1, 0]) circle(d=4.6, $fn=18);
    seg2d([-16, -13], [-6, -11], 1.6);
}

// ---------------------------------------------------------------------------
// Wreath: ordered pine clusters in a ring, small solid bow on the bottom edge.
// Center disk stays the 0.7 mm sheet (at least 30 mm across). Not a hole.
// Ring center in this drawing is the origin; wreath_shift places it on the panel.
// ---------------------------------------------------------------------------
wreath_shift = [0, 4];

module wreath_cluster() {
    hull() {
        circle(d=4.0, $fn=12);
        translate([0, 8.6]) circle(d=2.5, $fn=10);
    }
    hull() {
        translate([-1.1, 0.8]) circle(d=3.4, $fn=10);
        translate([-3.2, 6.2]) circle(d=2.4, $fn=10);
    }
    hull() {
        translate([1.1, 0.8]) circle(d=3.4, $fn=10);
        translate([3.2, 6.2]) circle(d=2.4, $fn=10);
    }
}
module wreath_foliage() {
    difference() {
        circle(d=42, $fn=96);
        circle(d=33, $fn=90);
    }
    for (a = [0:18:359])
        rotate(a) translate([0, 18.2]) wreath_cluster();
}
module wreath_bow() {
    // Two filled lobes and a knot on the lower rim, short tails below it.
    translate([-5.6, -22.4]) scale([1.12, 0.70]) circle(d=8.0, $fn=22);
    translate([ 5.6, -22.4]) scale([1.12, 0.70]) circle(d=8.0, $fn=22);
    translate([0, -22.6]) circle(d=4.6, $fn=20);
    seg2d([-1.5, -24.4], [-3.0, -30.2], 3.2);
    seg2d([ 1.5, -24.4], [ 3.0, -30.2], 3.2);
}
module wreath_body_2d() {
    translate(wreath_shift)
        front_of(1.15) {
            wreath_foliage();
            wreath_bow();
        }
}
module wreath_grooves_2d() {
    translate(wreath_shift) {
        for (a = [0:18:359])
            rotate(a) translate([0, 18.2]) seg2d([0, 1.2], [0, 7.2], 1.45);
        seg2d([-3.4, -22.4], [3.4, -22.4], 1.4);
        seg2d([-1.3, -24.6], [-2.6, -29.2], 1.35);
        seg2d([ 1.3, -24.6], [ 2.6, -29.2], 1.35);
    }
}

// ---------------------------------------------------------------------------
// Snowman: three balls, top hat, scarf, carrot, buttons, stick arms.
// ---------------------------------------------------------------------------
module arc_groove(cx, cy, r, a0, a1, w=1.8) {
    steps = 5;
    for (i = [0:steps - 1]) {
        aa = a0 + (a1 - a0) * i / steps;
        bb = a0 + (a1 - a0) * (i + 1) / steps;
        seg2d([cx + r*cos(aa), cy + r*sin(aa)],
              [cx + r*cos(bb), cy + r*sin(bb)], w);
    }
}

module snow_balls() {
    translate([0, -26]) circle(d=36, $fn=64);
    translate([0, 0]) circle(d=26, $fn=56);
    translate([0, 18]) circle(d=20, $fn=48);
}

module snow_arms() {
    seg2d([-11, 1], [-27, 12], 3.8);
    seg2d([-20, 8], [-24, 16], 3.1);
    seg2d([11, -1], [27, 9], 3.8);
    seg2d([20, 5], [25, 14], 3.1);
}

module snow_hat() {
    translate([0, 28.2]) scale([1, 0.22]) circle(d=32, $fn=48);
    translate([0, 36.4]) offset(r=1.5) square([14, 11], center=true);
}

module snow_carrot() {
    translate([7.2, 17.2])
        offset(r=1.15) polygon([[0, 2.6], [0, -2.2], [11, -0.2]]);
}

module snow_scarf() {
    // Laid onto the neck. Unioned with the balls so it cannot open a cream gap.
    translate([1, 11.5]) offset(r=1.8) square([20, 5.2], center=true);
    hull() {
        translate([-4, 11]) circle(d=6.2, $fn=16);
        translate([-15, 3]) circle(d=5.8, $fn=16);
        translate([-14.5, -8]) circle(d=5.2, $fn=14);
    }
}

module snowman_body_2d() {
    union() {
        snow_balls();
        snow_arms();
        snow_hat();
        snow_carrot();
        snow_scarf();
    }
}

module snowman_grooves_2d() {
    // The pair of dots that sat above these eyes was removed.
    // Coal smile: ends sit higher than the middle coal.
    translate([-5.0, 16.8]) circle(d=3.2, $fn=14);
    translate([ 0.0, 13.8]) circle(d=3.2, $fn=14);
    translate([ 4.8, 16.8]) circle(d=3.2, $fn=14);
    translate([0, 2.4]) circle(d=4.8, $fn=18);
    translate([0, -7.2]) circle(d=4.8, $fn=18);
    translate([0, -18.5]) circle(d=5.0, $fn=18);
    arc_groove(0, -26, 16.4, 58, 122, 1.5);
    // Bottom curve of the head, middle lower than the ends.
    arc_groove(0, 18, 8.4, 224, 316, 1.5);
    translate([0, 31.6]) square([10.5, 2.0], center=true);
    translate([-13.6, -1.5]) rotate(-68) square([1.5, 6.2], center=true);
    translate([11.5, 16.8]) rotate(-6) square([1.35, 4.2], center=true);
}

module icon_body_2d() {
    if (part == "tree") tree_body_2d();
    else if (part == "snowman") snowman_body_2d();
    else if (part == "reindeer") reindeer_body_2d();
    else if (part == "wreath") wreath_body_2d();
}

module icon_grooves_2d() {
    if (part == "tree") tree_grooves_2d();
    else if (part == "snowman") snowman_grooves_2d();
    else if (part == "reindeer") reindeer_grooves_2d();
    else if (part == "wreath") wreath_grooves_2d();
}

if (part == "blank") panel_blank_body();
else panel_litho();
