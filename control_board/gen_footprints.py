#!/bin/env python3
import sys
import os
from numpy import array

sys.path.append(os.path.join(sys.path[0], "../../kicad-footprint-generator/"))
from KicadModTree import *

LIBNAME='generated.pretty'
if not os.path.exists(LIBNAME):
    os.makedirs(LIBNAME)
lib=[]

def appendRectOutline(fp, s, e, ll=0.3, layer='F.SilkS'):
    #four L=shaped corners
    #TODO: optimize that
    c=[s[0], s[1]]
    fp.append(Line(start=c, end=[c[0]+ll, c[1]], layer=layer, width=0.12))
    fp.append(Line(start=c, end=[c[0], c[1]+ll], layer=layer, width=0.12))
    c=[e[0], s[1]]
    fp.append(Line(start=c, end=[c[0]-ll, c[1]], layer=layer, width=0.12))
    fp.append(Line(start=c, end=[c[0], c[1]+ll], layer=layer, width=0.12))
    c=[e[0], e[1]]
    fp.append(Line(start=c, end=[c[0]-ll, c[1]], layer=layer, width=0.12))
    fp.append(Line(start=c, end=[c[0], c[1]-ll], layer=layer, width=0.12))
    c=[s[0], e[1]]
    fp.append(Line(start=c, end=[c[0]+ll, c[1]], layer=layer, width=0.12))
    fp.append(Line(start=c, end=[c[0], c[1]-ll], layer=layer, width=0.12))

def appendPin1Dot(fp, at=[0, 0]):
    fp.append(Circle(center=at, radius=0.1, layer='F.SilkS', width=0.2))

def pin_header_2mm():
    #smd pin header 2x3 raster 2mm
    pin_h = Footprint("SMD_Female_Pin_Header_2x03_2mm")
    pin_h.append(Text(type='reference', text='REF**', at=[-3.9, 0], rotation=90, layer='F.SilkS'))
    pin_h.append(Text(type='value', text='VAL**', at=[3.9, 0], rotation=90, layer='F.Fab', hide=True))
    #courtyard
    pin_h.append(RectLine(start=[-3.2, -3.9], end=[3.2, 3.9], layer='F.CrtYd', width=0.05))
    #shape
    pin_h.append(RectLine(start=[-3, -2], end=[3, 2], layer='F.Fab', width=0.1))
    #placement
    appendRectOutline(pin_h, [-3.1, -2.1], [3.1, 2.1])
    appendPin1Dot(pin_h, at=[-2.9, -3])
    #pins
    pos = [-2, -2.475]
    for i in range(1, 7):
        pin_h.append(Pad(number=i, type=Pad.TYPE_SMT, layers=Pad.LAYERS_SMT, shape=Pad.SHAPE_RECT, width=0.1,
            at=pos, size=[0.85, 2.25]))
        pos = [pos[0], -pos[1]] if (i%2) else [pos[0]+2, -pos[1]]
    return pin_h

lib.append(pin_header_2mm())

def micromatch_conn_SMD(p):
    fp = Footprint("MicroMatch_%dp"% p)
    rr = 1.27
    A = rr*p + 2.02
    C = A - 1.5
    D = 5
    ul = array([-A/2, -D/2])
    fp.append(RectLine(start=[-A/2, -7.3/2], end=[A/2, 7.3/2], layer='F.CrtYd', width=0.05))
    fp.append(Text(type='reference', text='REF**', at=[-A/2-0.9, 0], rotation=90, layer='F.SilkS'))
    fp.append(Text(type='value', text='VAL**', at=[A/2+0.9, 0], rotation=90, layer='F.Fab', hide=True))
    appendRectOutline(fp, ul.tolist(), (ul*[-1,-1]).tolist(), ll=0.5)
    appendPin1Dot(fp, at=[-3.2, -3.1])

    #pins
    fp.append(PadArray(pincount=int(p/2), x_spacing=2*rr, center=[-rr/2, -2], initial=1, increment=2,
        type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[1.5, 2.5], layers=Pad.LAYERS_SMT))
    fp.append(PadArray(pincount=int(p/2), x_spacing=2*rr, center=[rr/2, 2], initial=2, increment=2,
        type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[1.5, 2.5], layers=Pad.LAYERS_SMT))

    #package
    fp.append(PolygoneLine(
        polygone=array([ul, ul+[A,0], ul+[A,D], ul+[0,D], ul+[0,D-1.25], ul+[(A-C)/2, D-1.25], ul+[(A-C)/2, 1.25], ul+[0, 1.25], ul]).tolist(),
        layer='F.Fab', width=0.1))
    fp.append(RectLine(start=[-C/2, -2], end=[C/2, 2], layer='F.Fab', width=0.1))

    return fp

lib.append(micromatch_conn_SMD(4))

def micromatch_conn_THT(p):
    fp = Footprint("THT_MicroMatch_%dp"% p)
    rr = 1.27
    A = rr*p + 2.02
    C = A - 1.5
    D = 5.2
    ul = array([-A/2, -D/2])
    fp.append(RectLine(start=[-A/2, -7.3/2], end=[A/2, 7.3/2], layer='F.CrtYd', width=0.05))
    fp.append(Text(type='reference', text='REF**', at=[-A/2-0.9, 0], rotation=90, layer='F.SilkS'))
    fp.append(Text(type='value', text='VAL**', at=[A/2+0.9, 0], rotation=90, layer='F.Fab', hide=True))
    appendRectOutline(fp, ul.tolist(), (ul*[-1,-1]).tolist(), ll=0.5)
    appendPin1Dot(fp, at=[-3.2, -3.1])

    #pins
    d = 0.81
    fp.append(PadArray(pincount=int(p/2), x_spacing=2*rr, center=[-rr/2, -2], initial=1, increment=2,
        type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, drill=d, size=[1.27, 1.27], layers=Pad.LAYERS_THT))
    fp.append(PadArray(pincount=int(p/2), x_spacing=2*rr, center=[rr/2, 2], initial=2, increment=2,
        type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, drill=d, size=[1.27, 1.27], layers=Pad.LAYERS_THT))

    #package
    fp.append(PolygoneLine(
        polygone=array([ul, ul+[A,0], ul+[A,D], ul+[0,D], ul+[0,D-1.25], ul+[(A-C)/2, D-1.25], ul+[(A-C)/2, 1.25], ul+[0, 1.25], ul]).tolist(),
        layer='F.Fab', width=0.1))
    fp.append(RectLine(start=[-C/2, -2], end=[C/2, 2], layer='F.Fab', width=0.1))

    return fp

lib.append(micromatch_conn_THT(4))

def jetson_tk1_expansion():
    fp = Footprint("Jetson_TK1_Expansion_Connector_J3A2")
    rr=2
    W=6
    L=50
    ul= array([-L/2, -W/2])
    fp.append(RectLine(start=[-L/2, -W/2], end=[L/2, W/2], layer='F.CrtYd', width=0.05))
    fp.append(Text(type='reference', text='REF**', at=[-L/2-0.9, 0], rotation=90, layer='F.SilkS'))
    fp.append(Text(type='value', text='VAL**', at=[L/2+0.9, 0], rotation=90, layer='F.Fab', hide=True))
    appendRectOutline(fp, ul.tolist(), (ul*[-1,-1]).tolist(), ll=2)
    appendPin1Dot(fp, at=[-25.4, -2.5])
    p=1
    pc=25
    d=1
    pad_sz = 0.89 + (2*0.05) + 0.2
    for i in [-2, 0, 2]:
        fp.append(PadArray(pincount=pc, x_spacing=rr, center=[0, i], initial=p, increment=3,
            type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=[pad_sz, pad_sz], drill=d, layers=Pad.LAYERS_THT))
        p = (p+1)
    return fp

lib.append(jetson_tk1_expansion())

#write  output file
for fp in lib:
    fh = KicadFileHandler(fp)
    fn = LIBNAME + '/' + fp.name + '.kicad_mod'
    print('Generating footprint:', fn)
    fh.writeFile(fn)
