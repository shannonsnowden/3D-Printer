// Seasonal Mantel Lantern v2 — Creality K1 Max
// Original design. Solid lithophane-style panels (thin glow sheet + raised relief).
// Support-free. Lift-off roof, top-loading slide-in panels.
// Units: mm.

/* [Global] */
$fn = 48;
part = "assembled";
// base | roof | panel_pumpkin | panel_cornucopia | panel_maple | panel_wheat
// panel_blank | panel_winter | panels_thanksgiving | assembled | exploded
// preview_front | preview_angled | preview_exploded | preview_panels

/* [Body — sturdy] */
body_outer        = 110;
post_size         = 16;      // thickened for handling
post_bead         = 1.4;     // decorative step (45° printable)
body_inner_h      = 112;
base_h            = 20;
base_rim          = 5;
base_chamfer      = 3;

/* [Channels / panels] */
panel_thick       = 1.8;     // rail + relief height
channel_clearance = 0.4;     // tweak ±0.1 after first fit
channel_depth     = 3.2;
channel_lead_in   = 5.0;     // generous funnel at top
panel_rail_w      = 4.0;
panel_field_t     = 0.7;     // continuous solid glow sheet (NO holes)
panel_h           = 105;
bottom_stop_h     = 2.8;
panel_edge_chamfer= 0.4;

/* [Roof — support-free] */
roof_overhang     = 10;
roof_skirt_h      = 10;
roof_pyramid_h    = 30;      // steep enough that faces are ~45°+ printable
roof_cap_h        = 6;
roof_cap_w        = 24;
ring_id           = 8;       // hanging hole
ring_thick        = 4;
ring_h            = 16;      // teardrop bail height (support-free)
vent_d            = 4.5;
vent_count        = 4;

/* [Tea light] */
tealight_well_d   = 42;
tealight_well_h   = 6;

/* Derived */
channel_w = panel_thick + channel_clearance;
panel_w   = body_outer - 2*post_size + 2*channel_depth;
opening_w = body_outer - 2*post_size;
post_h    = body_inner_h;
// Roof eaves print angle: rise of skirt underside chamfer
eave_chamfer = roof_overhang; // 45° from outer edge to post line

echo(str("panel_w=", panel_w, " panel_h=", panel_h));
echo(str("channel_w=", channel_w, " channel_clearance=", channel_clearance));
echo(str("post_size=", post_size, " field_t=", panel_field_t, " relief_t=", panel_thick));

// ---------------------------------------------------------------------------
module rounded_rect_2d(w, h, r) {
    offset(r=r) offset(r=-r) square([w, h], center=true);
}

// ---------------------------------------------------------------------------
// Posts — beads with 45° printable chamfers (no supports)
// ---------------------------------------------------------------------------
module post_profile(h) {
    s = post_size;
    b = post_bead;
    union() {
        translate([-s/2, -s/2, 0]) cube([s, s, h]);
        // Lower bead: ramp up then ramp down (printable)
        translate([0,0, h*0.10]) bead_band(s, b, 5);
        // Upper bead
        translate([0,0, h*0.78]) bead_band(s, b, 5);
        // Top locating collar (small, chamfered) — seats roof lip
        translate([0,0, h-3]) bead_band(s, b*0.6, 3);
    }
}

module bead_band(s, b, htot) {
    // Square band that grows/shrinks with 45° chamfers — no overhang
    half = htot/2;
    hull() {
        translate([-(s/2), -(s/2), 0]) cube([s, s, 0.05]);
        translate([-(s/2+b), -(s/2+b), half-0.05]) cube([s+2*b, s+2*b, 0.1]);
    }
    hull() {
        translate([-(s/2+b), -(s/2+b), half-0.05]) cube([s+2*b, s+2*b, 0.1]);
        translate([-(s/2), -(s/2), htot-0.05]) cube([s, s, 0.05]);
    }
}

module channel_cut(h) {
    w = channel_w;
    d = channel_depth;
    translate([-0.01, -w/2, -0.1])
        cube([d + 0.02, w, h + 0.2]);
    // Generous top funnel (widens ~2 mm total)
    translate([-0.01, 0, h - channel_lead_in])
        linear_extrude(height=channel_lead_in + 0.05, scale=[1, (w+2.0)/w])
            translate([0, -w/2]) square([d + 0.02, w]);
}

module corner_post_at(cx, cy, rot_z) {
    translate([cx, cy, base_h])
        rotate([0,0,rot_z])
        difference() {
            post_profile(post_h);
            translate([-post_size/2, 0, bottom_stop_h])
                mirror([1,0,0]) channel_cut(post_h - bottom_stop_h + 0.1);
            translate([0, -post_size/2, bottom_stop_h])
                rotate([0,0,90])
                mirror([1,0,0]) channel_cut(post_h - bottom_stop_h + 0.1);
        }
}

module base_deck() {
    ow = body_outer + 2*base_rim;
    difference() {
        union() {
            hull() {
                translate([0,0,base_chamfer])
                    linear_extrude(height=base_h-base_chamfer)
                        rounded_rect_2d(ow, ow, 5);
                linear_extrude(height=0.1)
                    rounded_rect_2d(ow-2*base_chamfer, ow-2*base_chamfer, 3.5);
            }
            // Upper molded lip
            translate([0,0,base_h-3.5])
                linear_extrude(height=3.5)
                    rounded_rect_2d(ow+2.5, ow+2.5, 5.5);
        }
        translate([0,0,base_h - tealight_well_h])
            cylinder(d=tealight_well_d, h=tealight_well_h + 0.1);
        translate([0,0,-0.1])
            cylinder(d=8, h=base_h + 0.2);
        // Decorative ring groove on deck
        translate([0,0,base_h-1.4])
            difference() {
                linear_extrude(height=1.5)
                    rounded_rect_2d(ow-7, ow-7, 3.5);
                linear_extrude(height=1.6)
                    rounded_rect_2d(ow-12, ow-12, 2.8);
            }
    }
}

module bottom_stops_fixed() {
    half = body_outer/2;
    inn = opening_w;
    t = 2.4;
    for (a = [0:90:270]) {
        rotate([0,0,a])
            translate([-inn/2 + 0.5, half - post_size - t, base_h])
                cube([inn - 1, t, bottom_stop_h]);
    }
}

module lantern_base() {
    half = body_outer/2;
    pc = half - post_size/2;
    union() {
        base_deck();
        corner_post_at( pc,  pc,   0);
        corner_post_at(-pc,  pc,  90);
        corner_post_at(-pc, -pc, 180);
        corner_post_at( pc, -pc, 270);
        bottom_stops_fixed();
    }
}

// ---------------------------------------------------------------------------
// Roof — 45° eave undersides + teardrop bail (support-free upright print)
// ---------------------------------------------------------------------------
module teardrop_bail_2d() {
    // Vertical hanging loop: circular hole, pointed top (self-supporting)
    // Outer teardrop, inner round hole
    difference() {
        hull() {
            circle(d=ring_id + 2*ring_thick);
            translate([0, ring_h/2]) circle(d=ring_thick*0.9);
        }
        circle(d=ring_id);
    }
}

module roof() {
    ow = body_outer + 2*roof_overhang;
    rebate = 0.45;                 // slip clearance over posts
    inner = body_outer + rebate*2;
    skirt = roof_skirt_h;
    // Pyramid slope: horizontal run from eaves to cap
    // run ≈ (ow - roof_cap_w)/2 ; rise = roof_pyramid_h
    // With ow=130, cap=24, run=53, rise=30 → angle atan(30/53)≈29° from horizontal
    // That's the OUTER face. For support-free we care about underside when printing
    // upright: the eaves underside must be ≤45° overhang.
    // Fix: solid eaves built as a 45° chamfer from outer rim up to the post line.

    difference() {
        union() {
            // ---- Support-free eaves: 45° chamfer block ----
            // Bottom of roof sits on bed? No — print upright with skirt bottom on bed.
            // Underside of overhang would face down toward bed... actually when printing
            // upright, skirt bottom is on the bed, so eaves grow outward as Z increases
            // OR we build eaves as a solid plate then pyramid.
            // Best: make the "eaves plate" thick enough that the outer perimeter
            // rises with a 45° outer chamfer, and the underside is FLAT on the print
            // bed for the central rebate area only — wait.
            //
            // Print orientation: roof upright, bottom of skirt on bed.
            // Geometry from bed up:
            //   z=0: smaller footprint (post-line) for locating lip walls
            //   z rises: expands at 45° to full eave width, then pyramid
            // That way there is NO downward-facing overhang.

            // Locating lip walls (slip over posts) — grow from bed
            // Outer solid grows at 45° from (body_outer) to ow over height eave_chamfer
            hull() {
                // at bed: just outside posts (for lip wall thickness)
                linear_extrude(height=0.2)
                    rounded_rect_2d(body_outer + 3, body_outer + 3, 2.5);
                // at eave height: full overhang
                translate([0,0, min(skirt, eave_chamfer)])
                    linear_extrude(height=0.2)
                        rounded_rect_2d(ow, ow, 5);
            }
            // Fill remainder of skirt to full ow if skirt > eave_chamfer
            if (skirt > eave_chamfer)
                translate([0,0, eave_chamfer])
                    linear_extrude(height=skirt - eave_chamfer)
                        rounded_rect_2d(ow, ow, 5);

            // Pyramid — faces slope inward (printable; no overhang)
            translate([0,0,skirt])
                hull() {
                    linear_extrude(height=0.2)
                        rounded_rect_2d(ow-1, ow-1, 4);
                    translate([0,0,roof_pyramid_h])
                        linear_extrude(height=0.2)
                            square([roof_cap_w, roof_cap_w], center=true);
                }

            // Raised cap
            translate([0,0,skirt + roof_pyramid_h])
                hull() {
                    linear_extrude(height=0.2)
                        square([roof_cap_w, roof_cap_w], center=true);
                    translate([0,0,roof_cap_h])
                        linear_extrude(height=0.2)
                            square([roof_cap_w-6, roof_cap_w-6], center=true);
                }

            // Teardrop hanging bail (vertical, pointed top = support-free)
            translate([0,0, skirt + roof_pyramid_h + roof_cap_h])
                rotate([90, 0, 0])
                    linear_extrude(height=ring_thick, center=true)
                        translate([0, ring_id/2 + ring_thick*0.55])
                            teardrop_bail_2d();
        }

        // Inner rebate — slips over posts (locating lip)
        // Leave ~2 mm wall at bottom edge for strength on bed perimeter
        translate([0,0,-0.1])
            linear_extrude(height=skirt - 2)
                rounded_rect_2d(inner, inner, 2);

        // Hollow under pyramid (weight + vents path)
        translate([0,0,skirt - 0.5])
            hull() {
                linear_extrude(height=0.2)
                    rounded_rect_2d(inner-2, inner-2, 2);
                translate([0,0,roof_pyramid_h-6])
                    cube([12,12,0.2], center=true);
            }

        // Side vents through eaves into cavity (horizontal holes — printable)
        for (i = [0:vent_count-1]) {
            ang = i*360/vent_count + 45;
            rotate([0,0,ang])
                translate([body_outer/2 - 1, 0, skirt*0.55])
                    rotate([0,90,0])
                        cylinder(d=vent_d, h=roof_overhang + 10, center=true);
        }
    }
}

// ---------------------------------------------------------------------------
// Panels — SOLID continuous glow sheet + raised relief (lithophane-style)
// NO holes, NO cutouts, NO lace.
// ---------------------------------------------------------------------------
module panel_blank_body() {
    // Rails at panel_thick + continuous field at panel_field_t
    w = panel_w; h = panel_h; t = panel_thick; rw = panel_rail_w; ft = panel_field_t;
    difference() {
        hull() {
            translate([0,0,panel_edge_chamfer])
                linear_extrude(height=t - 2*panel_edge_chamfer)
                    rounded_rect_2d(w, h, 1.2);
            linear_extrude(height=t)
                rounded_rect_2d(w - 2*panel_edge_chamfer, h - 2*panel_edge_chamfer, 1.0);
        }
        // Recess field from the TOP only → solid sheet of thickness ft remains
        translate([0,0,ft])
            linear_extrude(height=t + 0.1)
                rounded_rect_2d(w - 2*rw, h - 2*rw, 1.0);
    }
}

// ---------------------------------------------------------------------------
// v3 LITHOPHANE panels: three levels, never through the sheet
//   field 0.7 mm (bright) | groove floor 1.1 mm (glowing lines) | body 1.8 mm (dark)
// Each icon = <name>_body_2d() silhouette + <name>_grooves_2d() interior lines.
// ---------------------------------------------------------------------------
panel_groove_t = 1.1;
groove_w = 1.4;

module field_clip_2d(m=0) { rounded_rect_2d(panel_w - 2*panel_rail_w + 0.4 - 2*m, panel_h - 2*panel_rail_w + 0.4 - 2*m, 1.0); }

// children(0) behind, children(1) in front; a glowing gap separates them
module front_of(gap=1.4) { union() { difference() { children(0); offset(delta=gap) children(1); } children(1); } }

module icon_body_2d(n) {
    if (n=="turkey") turkey_body_2d();
    else if (n=="cornucopia") cornucopia_body_2d();
    else if (n=="pumpkin") pumpkin_body_2d();
    else if (n=="leaves") leaves_body_2d();
    else if (n=="pilgrim_hat") pilgrim_hat_body_2d();
    else if (n=="pumpkin_pie") pumpkin_pie_body_2d();
}
module icon_grooves_2d(n) {
    if (n=="turkey") turkey_grooves_2d();
    else if (n=="cornucopia") cornucopia_grooves_2d();
    else if (n=="pumpkin") pumpkin_grooves_2d();
    else if (n=="leaves") leaves_grooves_2d();
    else if (n=="pilgrim_hat") pilgrim_hat_grooves_2d();
    else if (n=="pumpkin_pie") pumpkin_pie_grooves_2d();
}
module icon_dark_2d(n) { offset(delta=0.05) offset(delta=-0.1) offset(delta=0.05) intersection() { field_clip_2d(); difference() { icon_body_2d(n); icon_grooves_2d(n); } } }
module icon_mid_2d(n)  { intersection() { field_clip_2d(); icon_body_2d(n); icon_grooves_2d(n); } }

module panel_litho(n) {
    union() {
        panel_blank_body();
        linear_extrude(height=panel_groove_t) intersection() { field_clip_2d(); icon_body_2d(n); }
        linear_extrude(height=panel_thick) icon_dark_2d(n);
    }
}

// ---- helpers ----
function bz(p,t) = pow(1-t,3)*p[0] + 3*pow(1-t,2)*t*p[1] + 3*(1-t)*t*t*p[2] + pow(t,3)*p[3];
function bz_ang(p,t) = let(a=bz(p,max(t-0.01,0)), b=bz(p,min(t+0.01,1))) atan2(b[1]-a[1], b[0]-a[0]);
module seg2d(a, b, w) { hull() { translate(a) circle(d=w,$fn=16); translate(b) circle(d=w,$fn=16); } }
module ring2d(w=groove_w) { difference() { offset(delta=w/2) children(); offset(delta=-w/2) children(); } }

// ===================== TURKEY (side view, facing left) =====================
tk_fan = [7,-8];
tk_angles = [for (i=[0:8]) 28 + i*15.5];
module tk_feather(a, L=30) { translate(tk_fan) rotate(a) hull() { circle(d=6,$fn=20); translate([L,0]) scale([1,0.62]) circle(d=14,$fn=36); } }
module tk_tail() { for (a=tk_angles) tk_feather(a); }
module tk_body() { translate([-1,-15]) scale([1,0.82]) circle(d=40,$fn=72); }
module tk_head() {
    seg2d([-11,-8], [-19,6], 9);
    translate([-20,9]) circle(d=11,$fn=40);
    polygon([[-24.5,11.5],[-32,8.5],[-24.5,6.5]]);                 // beak
    seg2d([-25.5,12.5], [-28.5,4.5], 2.6);                          // snood
    hull() { translate([-22.5,4]) circle(d=4.6,$fn=20); translate([-23.5,-3]) circle(d=4,$fn=20); } // wattle
}
module tk_legs() {
    for (x=[-7,4]) {
        seg2d([x,-27], [x-1,-39], 3);
        seg2d([x-1,-39], [x-6,-42], 2.4);
        seg2d([x-1,-39], [x-1,-43], 2.4);
        seg2d([x-1,-39], [x+4,-42], 2.4);
    }
}
module turkey_body_2d() { translate([2.5,1]) scale(0.93) front_of() { tk_tail(); union() { tk_body(); tk_head(); tk_legs(); } } }
module turkey_grooves_2d() { translate([2.5,1]) scale(0.93) union() {
    // feather separators
    for (i=[0:7]) let(a=(tk_angles[i]+tk_angles[i+1])/2)
        translate(tk_fan) rotate(a) translate([13,-groove_w/2]) square([27,groove_w]);
    // eye-band arc across every feather
    intersection() { tk_tail(); translate(tk_fan) ring2d() circle(r=28,$fn=96); }
    // wing
    translate([3,-14]) rotate(-12) ring2d() scale([1,0.55]) circle(d=24,$fn=60);
    for (k=[0:2]) translate([3+k*3,-17-k*0.5]) rotate(-12) translate([0,-groove_w/2]) square([9,groove_w]);
    // eye
    translate([-20.5,11]) circle(d=2.4,$fn=16);
    // neck/body join
    translate([-12,-6]) rotate(-60) translate([0,-groove_w/2]) square([7,groove_w]);
}}

// ===================== CORNUCOPIA =====================
hn_p = [[-16,30],[-38,24],[-32,-30],[6,-18]];
function hn_r(t) = 1.6 + 13.5*pow(t,1.35);
module hn_horn() {
    N=40;
    for (i=[0:N-1]) hull() {
        translate(bz(hn_p,i/N)) circle(r=hn_r(i/N),$fn=40);
        translate(bz(hn_p,(i+1)/N)) circle(r=hn_r((i+1)/N),$fn=40);
    }
    translate(bz(hn_p,1)) rotate(bz_ang(hn_p,1)) scale([0.42,1]) circle(r=hn_r(1)+1.5,$fn=48); // mouth rim
}
module hn_apple() { translate([22,-4]) { scale([1,0.92]) circle(d=17,$fn=56); seg2d([0,7],[1.5,11],2.4); translate([5,11]) rotate(20) scale([1,0.45]) circle(d=8,$fn=24); } }
module hn_grape(i) { cx=[-4,0,4,-2,2,0]; cy=[0,0,0,-4,-4,-8]; translate([26+cx[i], -18+cy[i]]) circle(d=5.2,$fn=24); }
module hn_grapes() { for (i=[0:5]) hn_grape(i); seg2d([26,-16],[29,-11],2.2); }
module hn_pear() { translate([17,17]) { scale([1.25,1]) circle(d=13,$fn=48); hull() { translate([-1.4,5]) square([2.8,1]); translate([0,10]) rotate(-20) square([2.6,1]); } } }
module hn_wheat(base, ang) {
    translate(base) rotate(ang) {
        translate([-1.1,0]) square([2.2,12]);
        for (k=[0:3]) for (s=[-1,1]) translate([s*2.1, 13+k*4.3]) rotate(-s*25) scale([0.55,1]) circle(d=6.8,$fn=20);
        translate([0,31.5]) scale([0.55,1]) circle(d=6.5,$fn=20);
    }
}
module hn_wheats() { hn_wheat([2,-6], 12); hn_wheat([6,-4], -18); }
module hn_produce() { hn_wheats(); hn_pear(); hn_apple(); hn_grapes(); }
module cornucopia_body_2d() {
    front_of() {
        front_of() { front_of() { hn_horn(); hn_wheats(); } hn_pear(); }
        union() { hn_apple(); hn_grapes(); }
    }
}
module cornucopia_grooves_2d() {
    // spiral wicker wraps across the horn (only where horn is visible)
    intersection() {
        difference() { offset(delta=-1.6) hn_horn(); offset(delta=1.4) hn_produce(); }
        union() for (t=[0.34,0.46,0.57,0.67,0.76,0.85,0.93]) translate(bz(hn_p,t)) rotate(bz_ang(hn_p,t)+80) square([groove_w,2*hn_r(t)+3],center=true);
    }
    // mouth opening (hollow glows)
    difference() {
        translate(bz(hn_p,1)) rotate(bz_ang(hn_p,1)) scale([0.42,1]) circle(r=hn_r(1)-1.5,$fn=48);
        offset(delta=1.4) hn_produce();
    }
    translate([17,17]) intersection() { offset(delta=-2) scale([1.25,1]) circle(d=13,$fn=48); for (a=[4]) ring2d(1.3) scale([a/6.5,1]) circle(d=13,$fn=48); }
    // apple highlight + grain center lines
    translate([22,-4]) intersection() { ring2d() circle(d=10,$fn=40); translate([-10,0]) square([10,10]); }
    for (w=[[[2,-6],12],[[6,-4],-18]]) translate(w[0]) rotate(w[1]) translate([-0.6,13]) square([1.2,17]);
    // pear crease
    
}

// ===================== PUMPKIN =====================
pk_lobes = [[0,20,50],[9,20,49],[-9,20,49],[18,20,46],[-18,20,46],[25,17,40],[-25,17,40]];
module pk_shape() { translate([0,-8]) for (l=pk_lobes) translate([l[0],0]) scale([l[1]/l[2],1]) circle(d=l[2],$fn=64); }
module pk_stem() { hull() { translate([-3.5,14]) square([7,1]); translate([1,26]) rotate(-20) square([5,2]); } }
module pk_tendril() { translate([10,23]) difference() { circle(r=5,$fn=40); circle(r=2.6,$fn=40); translate([-6,-6]) square([6,6]); } }
module pk_leaf() { translate([-14,23]) rotate(25) scale([1.5,0.75]) circle(d=14,$fn=40); }
module pumpkin_body_2d() { union() { pk_shape(); pk_stem(); pk_tendril(); } }
module pumpkin_grooves_2d() {
    // 6 curved ribs → 7 lobes
    intersection() {
        offset(delta=-2.4) pk_shape();
        translate([0,-8]) for (a=[4.5,13.5,21.5]) ring2d() scale([a/25,1]) circle(d=50,$fn=72);
    }
    // stem stripe + leaf vein
    translate([0.2,17]) rotate(-10) square([1.2,8]);
}

// ===================== FALLING MAPLE LEAVES =====================
// unit maple (right half, tip up, base at origin-ish); mirrored for left half
mp_half = [[0,1.0],[0.11,0.76],[0.24,0.84],[0.19,0.46],[0.46,0.60],[0.52,0.50],[0.90,0.60],
           [0.76,0.36],[0.84,0.27],[0.42,0.14],[0.72,-0.06],[0.46,-0.10],[0.42,-0.22],[0.07,-0.12],[0.06,-0.16]];
mp_poly = concat(mp_half, [for (i=[len(mp_half)-1:-1:0]) [-mp_half[i][0], mp_half[i][1]]]);
mp_tips = [[0,0.92],[0.80,0.56],[-0.80,0.56],[0.62,-0.04],[-0.62,-0.04]];
// leaves: [center, size, rotation]  (listed back → front)
lv = [[[-8,22],25,16], [[23,32],13,-50], [[15,1],20,-30], [[-15,-17],18,38], [[14,-31],16,-14]];
function lvp(L,p) = let(a=L[2], q=L[1]*p) L[0] + [q[0]*cos(a)-q[1]*sin(a), q[0]*sin(a)+q[1]*cos(a)];
module lv_leaf(L) {
    translate(L[0]) rotate(L[2]) scale(L[1]) polygon(mp_poly);
    seg2d(lvp(L,[0,-0.1]), lvp(L,[0.05,-0.5]), max(2.4, L[1]*0.11));   // stem
}
module lv_veins(L) {
    intersection() {
        offset(delta=-1.9) translate(L[0]) rotate(L[2]) scale(L[1]) polygon(mp_poly);
        union() for (t=mp_tips) seg2d(lvp(L,[0,0.0]), lvp(L,t), groove_w);
    }
}
module lv_stack(k) { if (k==0) lv_leaf(lv[0]); else front_of() { lv_stack(k-1); lv_leaf(lv[k]); } }
module leaves_body_2d() { lv_stack(len(lv)-1); }
module leaves_grooves_2d() {
    for (k=[0:len(lv)-1]) difference() {
        lv_veins(lv[k]);
        if (k<len(lv)-1) for (j=[k+1:len(lv)-1]) offset(delta=1.4) lv_leaf(lv[j]);
    }
}

// ===================== PILGRIM HAT (capotain, slight 3/4 view) =====================
ph_crown = [[-19,-12],[19,-12],[15.5,30],[13,33],[-13,33],[-15.5,30]];
module ph_brim() { translate([0,-14]) scale([1,0.30]) circle(d=74,$fn=96); }
module ph_crown2d() { polygon(ph_crown); translate([0,30]) scale([1,0.28]) circle(d=29,$fn=60); }
module ph_band() { intersection() { ph_crown2d(); translate([-30,-9]) square([60,11]); } }
module ph_buckle_out() { translate([0,-3.5]) square([14,13],center=true); }
module ph_buckle_in()  { translate([0,-3.5]) square([7.4,6.4],center=true); }
module pilgrim_hat_body_2d() {
    difference() { translate([0,6]) union() { ph_brim(); ph_crown2d(); } translate([0,6]) ph_buckle_in(); }
}
module pilgrim_hat_grooves_2d() { translate([0,6]) {
    // hatband stripe (glows amber) except under buckle frame
    difference() { ph_band(); offset(delta=0) ph_buckle_out(); }
    // front brim edge where crown sits on the brim
    intersection() { translate([0,-14]) ring2d() scale([1,0.30]) circle(d=62,$fn=96); translate([-40,-40]) square([80,26]); }
    // top-of-crown ellipse rim
    intersection() { translate([0,30]) ring2d() scale([1,0.28]) circle(d=25,$fn=60); translate([-20,28]) square([40,10]); }
    // crown highlight crease
    translate([-9,4]) rotate(-5) square([groove_w,24]);
}}

// ===================== PUMPKIN PIE SLICE (top-down wedge, tip down) =====================
pp_tip = [0,-38]; pp_R = 64; pp_half = 29;
module pp_wedge(r) { translate(pp_tip) intersection() { circle(r=r,$fn=180); polygon([[0,0], [r*1.2*sin(-pp_half), r*1.2*cos(pp_half)], [0,r*1.3], [r*1.2*sin(pp_half), r*1.2*cos(pp_half)]]); } }
module pp_fill() { pp_wedge(pp_R-8); }
module pp_crust() {
    translate(pp_tip) {
        intersection() { difference() { circle(r=pp_R,$fn=180); circle(r=pp_R-9,$fn=180); }
                         rotate(90-pp_half-2) square([200,200]); rotate(90+pp_half+2) translate([0,-200]) square([200,200]); }
        for (k=[0:8]) let(a=90-pp_half+k*(2*pp_half)/8) translate([pp_R*cos(a), pp_R*sin(a)]) circle(d=8.5,$fn=32); // fluted crimps
    }
}
module pp_cream() { translate([0,6]) { scale([1.25,1]) circle(d=17,$fn=48); translate([0,6]) scale([1.2,1]) circle(d=12,$fn=40); translate([1.5,11]) circle(d=6,$fn=24); } }
module pumpkin_pie_body_2d() { translate([0,-1]) front_of() { front_of() { pp_fill(); pp_crust(); } pp_cream(); } }
module pumpkin_pie_grooves_2d() { translate([0,-1]) {
    // crimp separators between flutes + inner crust edge line
    translate(pp_tip) for (k=[0:7]) let(a=90-pp_half+(k+0.5)*(2*pp_half)/8) seg2d([(pp_R-3)*cos(a),(pp_R-3)*sin(a)], [(pp_R+3.5)*cos(a),(pp_R+3.5)*sin(a)], 1.3);
    // thin bottom-crust rim along the two cut edges
    difference() { intersection() { ring2d() offset(delta=-3.2) pp_fill(); translate(pp_tip) circle(r=pp_R-13,$fn=120); } offset(delta=1.4) pp_cream(); }
    // cream swirl lines
    translate([0,6]) intersection() { ring2d(1.3) scale([1.25,1]) circle(d=10,$fn=40); translate([-12,-12]) square([24,11]); }
    translate([0,12]) intersection() { ring2d(1.3) scale([1.2,1]) circle(d=6,$fn=32); translate([-6,-6]) square([12,5]); }
}}

// ---- Thanksgiving panels ----
module panel_turkey()     { panel_litho("turkey"); }
module panel_cornucopia() { panel_litho("cornucopia"); }
module panel_pumpkin()    { panel_litho("pumpkin"); }
module panel_leaves()     { panel_litho("leaves"); }
module panel_pilgrim_hat() { panel_litho("pilgrim_hat"); }
module panel_pumpkin_pie() { panel_litho("pumpkin_pie"); }
module panel_winter()     { panel_with_relief() art_winter(); }
module panel_blank()      { panel_blank_body(); }
module panel_harvest()    { panel_pumpkin(); }

module art_winter() {
    union() {
        translate([0,-12]) scale(1.15) union() {
            translate([0,10]) polygon([[0,14],[-12,0],[12,0]]);
            translate([0,2]) polygon([[0,12],[-15,-2],[15,-2]]);
            translate([0,-6]) polygon([[0,12],[-18,-4],[18,-4]]);
            translate([-2.2,-18]) square([4.4,10]);
        }
        translate([0,30]) star_2d(9, 0.42);
        translate([-26,18]) snowflake_2d(11);
        translate([26,12]) snowflake_2d(9);
        translate([22,-28]) snowflake_2d(7);
        translate([-20,-30]) snowflake_2d(6);
    }
}
module snowflake_2d(r=16) {
    union() {
        for (a=[0:60:300]) rotate(a) {
            translate([-1.1,0]) square([2.2,r]);
            translate([0,r*0.55]) rotate(45) translate([-0.8,0]) square([1.6,r*0.28]);
            translate([0,r*0.55]) rotate(-45) translate([-0.8,0]) square([1.6,r*0.28]);
        }
        circle(d=5);
    }
}
module star_2d(r=10, inner=0.4) {
    points = [for (i=[0:9]) let(a=i*36-90, rad=(i%2==0)?r:r*inner) [rad*cos(a), rad*sin(a)]];
    polygon(points);
}
module panel_with_relief() {
    // children() = 2D art; extruded as raised relief on the glow sheet
    w = panel_w; h = panel_h; t = panel_thick; rw = panel_rail_w;
    union() {
        panel_blank_body();
        intersection() {
            linear_extrude(height=t)
                rounded_rect_2d(w - 2*rw + 0.4, h - 2*rw + 0.4, 1.0);
            linear_extrude(height=t)
                children();
        }
    }
}


// ---------------------------------------------------------------------------
// Assembly
// ---------------------------------------------------------------------------
module panel_in_bay(side=0, z_lift=0) {
    half = body_outer/2;
    y_mid = (half - post_size) + channel_depth/2;
    rotate([0,0, side*90])
        translate([0, y_mid - panel_thick/2, base_h + bottom_stop_h + panel_h/2 + z_lift])
            rotate([-90,0,0]) mirror([0,1,0]) children();
}
module panel_in_bay_preview(side=0, z_lift=0, outset=5) {
    half = body_outer/2;
    y_mid = (half - post_size) + channel_depth/2 + outset;
    rotate([0,0, side*90])
        translate([0, y_mid - panel_thick/2, base_h + bottom_stop_h + panel_h/2 + z_lift])
            rotate([-90,0,0]) mirror([0,1,0]) children();
}
tg_names = ["turkey","pumpkin_pie","leaves","pilgrim_hat"];   // shown in lantern
tg_all = ["turkey","cornucopia","pumpkin","leaves","pilgrim_hat","pumpkin_pie"];

module assembled() {
    lantern_base();
    translate([0,0, base_h + post_h - (roof_skirt_h - 2)]) roof();
    for (i=[0:3]) panel_in_bay(i) panel_litho(tg_names[i]);
}

// Preview colouring: mode 0 = two-tone (ivory/tan/sienna), 1 = candle backlight sim
module panel_color_preview(n, mode=0) {
    c_field = mode==0 ? "Ivory" : [1.0,0.93,0.62];
    c_mid   = mode==0 ? "Tan"   : [0.85,0.52,0.18];
    c_dark  = mode==0 ? "Sienna": [0.27,0.13,0.05];
    w = panel_w; h = panel_h; rw = panel_rail_w;
    color(c_field) linear_extrude(height=panel_field_t) rounded_rect_2d(w, h, 1.0);
    color(c_dark) linear_extrude(height=panel_thick) difference() { rounded_rect_2d(w, h, 1.0); rounded_rect_2d(w-2*rw, h-2*rw, 1.0); }
    color(c_mid) linear_extrude(height=panel_groove_t) intersection() { field_clip_2d(); icon_body_2d(n); }
    color(c_dark) linear_extrude(height=panel_thick) icon_dark_2d(n);
}

module assembled_preview() {
    color("BurlyWood") lantern_base();
    color("BurlyWood") translate([0,0, base_h + post_h - (roof_skirt_h - 2)]) roof();
    for (i=[0:3]) panel_in_bay_preview(i) panel_color_preview(tg_names[i]);
}
module exploded_view() {
    color("BurlyWood") lantern_base();
    color("BurlyWood") translate([0,0, base_h + post_h - (roof_skirt_h - 2) + 58]) roof();
    for (i=[0:3]) panel_in_bay_preview(i, z_lift=(i==0?50:0), outset=(i==0?5:5)) panel_color_preview(tg_names[i]);
}
module panels_thanksgiving() {
    gap = panel_w + 14;
    for (i=[0:5]) translate([(i%3-1)*gap,(i<3?1:-1)*(panel_h+14)/2,0]) panel_litho(tg_all[i]);
}
module panels_thanksgiving_preview(mode=0) {
    gap = panel_w + 14;
    for (i=[0:5]) translate([(i%3-1)*gap,(i<3?1:-1)*(panel_h+14)/2,0]) panel_color_preview(tg_all[i], mode);
}

// ---------------------------------------------------------------------------
if (part == "base") lantern_base();
else if (part == "roof") roof();
else if (part == "panel_turkey") panel_turkey();
else if (part == "panel_cornucopia") panel_cornucopia();
else if (part == "panel_pumpkin" || part == "panel_harvest") panel_pumpkin();
else if (part == "panel_leaves") panel_leaves();
else if (part == "panel_pilgrim_hat") panel_pilgrim_hat();
else if (part == "panel_pumpkin_pie") panel_pumpkin_pie();
else if (part == "panel_winter") panel_winter();
else if (part == "panel_blank") panel_blank();
else if (part == "panels_thanksgiving" || part == "panels_layout") panels_thanksgiving();
else if (part == "preview_panels") panels_thanksgiving_preview(0);
else if (part == "preview_panels_backlit") panels_thanksgiving_preview(1);
else if (part == "assembled") assembled();
else if (part == "exploded" || part == "preview_exploded") exploded_view();
else if (part == "preview_front" || part == "preview_angled") assembled_preview();
