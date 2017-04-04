KISYSMOD=/usr/share/kicad/library/

%.net: %.py
	python2 $<

all: schematic.net

clean:
	-rm -rf schematic.log schematic.net skidl.log
