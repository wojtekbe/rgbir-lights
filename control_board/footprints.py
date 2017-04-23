import sys
import os

sys.path.append(os.path.join(sys.path[0], "../../kicad-footprint-generator/"))
from KicadModTree import *

LIBNAME='generated.pretty'
if not os.path.exists(LIBNAME):
    os.makedirs(LIBNAME)

def appendRectOutline(fp, s, e, lw=0.3, layer='F.SilkS'):
    #four L=shaped corners
    c=[s[0], s[1]]
    fp.append(Line(start=c, end=[c[0]+lw, c[1]], layer=layer, width=0.12))
    fp.append(Line(start=c, end=[c[0], c[1]+lw], layer=layer, width=0.12))
    c=[e[0], s[1]]
    fp.append(Line(start=c, end=[c[0]-lw, c[1]], layer=layer, width=0.12))
    fp.append(Line(start=c, end=[c[0], c[1]+lw], layer=layer, width=0.12))
    c=[e[0], e[1]]
    fp.append(Line(start=c, end=[c[0]-lw, c[1]], layer=layer, width=0.12))
    fp.append(Line(start=c, end=[c[0], c[1]-lw], layer=layer, width=0.12))
    c=[s[0], e[1]]
    fp.append(Line(start=c, end=[c[0]+lw, c[1]], layer=layer, width=0.12))
    fp.append(Line(start=c, end=[c[0], c[1]-lw], layer=layer, width=0.12))

#smd pin header 2x3 raster 2mm
name = "SMD_Female_Pin_Header_2x03_2mm"
pin_h = Footprint(name)
pin_h.append(Text(type='reference', text='REF**', at=[-3.9, 0], rotation=90, layer='F.SilkS'))
pin_h.append(Text(type='value', text='VAL**', at=[3.9, 0], rotation=90, layer='F.Fab', hide=True))

#courtyard
pin_h.append(RectLine(start=[-3.2, -3.9], end=[3.2, 3.9], layer='F.CrtYd', width=0.05))

#shape
pin_h.append(RectLine(start=[-3, -2], end=[3, 2], layer='F.Fab', width=0.1))

#placement
appendRectOutline(pin_h, [-3.1, -2.1], [3.1, 2.1])
pin_h.append(Circle(center=[-2.9, -3], radius=0.12, layer='F.SilkS'))

#pins
pos = [-2, -2.475]
for i in range(1, 7):
    pin_h.append(Pad(number=i, type=Pad.TYPE_SMT, layers=Pad.LAYERS_SMT, shape=Pad.SHAPE_RECT, width=0.1,
        at=pos, size=[0.85, 2.25]))
    pos = [pos[0], -pos[1]] if (i%2) else [pos[0]+2, -pos[1]]

#write  output file
fh = KicadFileHandler(pin_h)
fh.writeFile(LIBNAME + '/' + name + '.kicad_mod')
