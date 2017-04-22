KICAD_LIB=/usr/share/kicad/library/
PCBNAME=lights

netlist: $(PCBNAME).net
.PHONY: clean netlist

%.net: %.py
	KISYSMOD=$(KICAD_LIB) python2 $<

clean:
	-rm -rf $(PCBNAME).log $(PCBNAME).net skidl.log *.erc *.kicad_pcb-bak $(PCBNAME)_lib_sklib.py
