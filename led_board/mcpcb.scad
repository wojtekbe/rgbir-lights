module mcpcb(drill, num_holes)
{
	linear_extrude(2) {
		difference() {
			union() {
				circle (r=24/2);
				translate([24.5/2, 0, 0])
					square(size=[24.5, 10], center=true);
			}
			for (i=[0:num_holes-1]) {
				rotate([0, 0, i*360/num_holes])
					translate([9.3, 0, 0])
						circle(drill/2);
			}
		}
	}
}

module mcpcb_pattern(n, r)
{
	for (i=[0:n-1]) {
		rotate([0, 0, i*360/n])
			translate([r, 0, 0])
				mcpcb(drill = 2.2, num_holes = 6);
	}
}

module holder_board(d)
{
	drill = 4;
	linear_extrude(2) {
		difference() {
			circle(d/2);
			for (i=[0:4])
				rotate([0, 0, 45+(i*90)])
					translate([(d/2)-6, 0, 0])
						circle(drill/2);
			circle(drill/2);
		}
	}
}

color("green") holder_board(65);
translate([0, 0, 2]) {
	color("Gold") mcpcb_pattern(4, 18);
}
