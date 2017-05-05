module lens()
{
	/* http://www.ledil.com/lett/2d_datasheet/586ab7-LE1-series%20datasheet_no-tape.pdf */
	color("White", 0.5) cylinder(d=21.56, h=14.8);
}

module mcpcb(drill, num_holes)
{
	/* mcpcb */
	color("Silver") linear_extrude(1.7) {
		difference() {
			union() {
				circle (r=24/2);
				translate([24.5/2, 0, 0])
					square(size=[24.5, 9.7], center=true);
			}
			for (i=[0:num_holes-1]) {
				rotate([0, 0, i*360/num_holes])
					translate([9.3, 0, 0])
						circle(drill/2);
			}
		}
	}

	/* connector */
	color("Red") translate([19, 0, 1.7+(5.1/2)]) {
		cube([4, 5.6, 5.1], center=true);
	}

	/* lens */
	translate([0, 0, 1.7]) lens();

}

module mcpcb_pattern(n, r)
{
	for (i=[0:n-1]) {
		rotate([0, 0, i*360/n])
			translate([r, 0, 0])
				mcpcb(drill = 2.2, num_holes = 6);
	}
}


module holder_board(d, D)
{
	color("Green") linear_extrude(2) {
		difference() {
			circle(r=D);
			circle(r=d);
		}
		n = 6;
		for (i=[0:n-1]) {
			rotate([0, 0, i*360/n])
				translate([d, 0, 0])
					square([9.7, 9.7], center=true);
		}
	}
}

holder_board(26+19, 26+19+20);
translate([0, 0, -6]) mcpcb_pattern(6, 26);
