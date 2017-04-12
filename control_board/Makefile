KICAD_LIB=/usr/share/kicad/library/
PCBNAME=lights

%.net: %.py
	KISYSMOD=$(KICAD_LIB) python2 $<

all: $(PCBNAME).net

clean:
	-rm -rf $(PCBNAME).log $(PCBNAME).net skidl.log *.erc *.kicad_pcb-bak $(PCBNAME)_lib_sklib.py
