// Shared lithophane panel library.
// Final panel size is authored here. Do not scale the exported STL.
//
// Side rails match the resized Thanksgiving meshes: the legacy blank
// (width 84.4 mm, 4 mm rails, 0.4 mm edge chamfer) is scaled in X only,
// by 77.5/84.4, inside this file. Icons are drawn in the final frame
// and are not scaled.

panel_w = 77.5;
panel_h = 105;
panel_thick = 1.8;
panel_field_t = 0.7;
panel_groove_t = 1.1;
panel_rail_w = 4.0;
panel_edge_chamfer = 0.4;
legacy_panel_w = 84.4;
rail_x_scale = panel_w / legacy_panel_w;
groove_w = 1.55;

$fn = 48;

module rounded_rect_2d(w, h, r) {
    offset(r=r) offset(r=-r) square([w, h], center=true);
}

module panel_blank_body_at_width(w) {
    h = panel_h;
    t = panel_thick;
    rw = panel_rail_w;
    ft = panel_field_t;
    c = panel_edge_chamfer;
    difference() {
        hull() {
            translate([0, 0, c])
                linear_extrude(height=t - 2*c)
                    rounded_rect_2d(w, h, 1.2);
            linear_extrude(height=t)
                rounded_rect_2d(w - 2*c, h - 2*c, 1.0);
        }
        translate([0, 0, ft])
            linear_extrude(height=t + 0.1)
                rounded_rect_2d(w - 2*rw, h - 2*rw, 1.0);
    }
}

module panel_blank_body() {
    scale([rail_x_scale, 1, 1])
        panel_blank_body_at_width(legacy_panel_w);
}

module field_clip_2d(m=0) {
    scale([rail_x_scale, 1])
        rounded_rect_2d(legacy_panel_w - 2*panel_rail_w + 0.4 - 2*m,
                        panel_h - 2*panel_rail_w + 0.4 - 2*m,
                        1.0);
}

module front_of(gap=1.5) {
    union() {
        difference() {
            children(0);
            offset(delta=gap) children(1);
        }
        children(1);
    }
}

module seg2d(a, b, w=1.55) {
    hull() {
        translate(a) circle(d=w, $fn=14);
        translate(b) circle(d=w, $fn=14);
    }
}

// Holiday files define icon_body_2d() and icon_grooves_2d().
module icon_dark_2d() {
    offset(delta=0.05) offset(delta=-0.1) offset(delta=0.05)
        intersection() {
            field_clip_2d();
            difference() {
                icon_body_2d();
                icon_grooves_2d();
            }
        }
}

module panel_litho() {
    union() {
        panel_blank_body();
        linear_extrude(height=panel_groove_t)
            intersection() {
                field_clip_2d();
                icon_body_2d();
            }
        linear_extrude(height=panel_thick) icon_dark_2d();
    }
}
