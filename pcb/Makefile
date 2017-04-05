KICAD_LIB=/usr/share/kicad/library/

%.net: %.py
	KISYSMOD=$(KICAD_LIB) python2 $<

all: schematic.net

clean:
	-rm -rf schematic.log schematic.net skidl.log
