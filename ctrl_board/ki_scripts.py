from pcbnew import wxPoint, GetBoard, TRACK, PCB_LAYER_ID_COUNT, DRAWSEGMENT
from math import sin, cos, radians, degrees, atan2, sqrt

PREC=2

def wxpoint_to_list(wxpoint):
    return [round(wxpoint.x/1e6, PREC), round(wxpoint.y/1e6, PREC)]

def list_to_wxpoint(l):
    return wxPoint(int(l[0]*1e6), int(l[1]*1e6))

def to_polar(xy):
    rho = round(sqrt(xy[0]**2 + xy[1]**2), PREC)
    theta = round(degrees(atan2(xy[1], xy[0])), PREC)
    return [rho, theta]

def to_cart(rt):
    x = round(rt[0] * cos(radians(rt[1])), PREC)
    y = round(rt[0] * sin(radians(rt[1])), PREC)
    return [x, y]

def rot(v, a):
    ret = [round(v[0]*cos(radians(a))-v[1]*sin(radians(a)), PREC),
            round(v[0]*sin(radians(a))+v[1]*cos(radians(a)), PREC)]
    return ret

def ls_tracks():
    netcodes = pcb.GetNetsByNetcode()
    for netcode, net in netcodes.items():
        tracks = pcb.TracksInNet(netcode)
        print("{} {} {}".format(netcode, net.GetNetname(), [[wxpoint_to_list(t.GetStart()) for t in tracks], [wxpoint_to_list(t.GetEnd()) for t in tracks]]))

def gen_bom(fname='bom.txt'):
    bom = {}
    for r,m in M.iteritems():
        pack = m.get_value() + ':' + m.get_package()
        if pack not in bom:
            bom[pack] = []
        bom[pack].append(r)

    with open(fname, 'w') as f:
        for p,R in bom.iteritems():
            ref_list = ''
            for n,ref in enumerate(R):
                ref_list += (ref + ',') if (n < (len(R)-1)) else ref
            f.write("%dx %s %s\n" %(len(R), p, ref_list))

def get_net(n):
    if isinstance(n, int):
        nets = pcb.GetNetsByNetcode()
    if isinstance(n, basestring):
        nets = pcb.GetNetsByName()
    return nets[n]

def add_track(net, start, end, layer=0):
    t = TRACK(pcb)
    pcb.Add(t)
    t.SetNet(get_net(net))
    t.SetStart(list_to_wxpoint(start))
    t.SetEnd(list_to_wxpoint(end))
    t.SetLayer(layer)
    print("{} {} {} {}".format(net, start, end, pcb.GetLayerName(layer)))

def add_arc_track(net, r, start_angle, end_angle, segments=6, layer=0):
    da = ((end_angle - start_angle) / float(segments))
    for s in range(segments):
        sa = start_angle + (s * da)
        ea = start_angle + ((s + 1) * da)
        add_track(net, to_cart([r, sa],), to_cart([r, ea]), layer)

def circle_pattern(mods, refmod):
    n = len(mods) + 1
    da = 360 / float(n)
    print(da)
    for i,m in enumerate(mods):
        m.align(refmod)
        m.rotate((i+1)*da)

class PolyLine:
    def __init__(self, pcb, pts, layer=0, width=0.2):
        self.pcb = pcb
        self.pts = pts
        self.segments = []
        self.layer = layer
        self.width = width
        self.render()

    def render(self):
        for i in range(len(self.pts)-1):
            seg = DRAWSEGMENT(self.pcb)
            self.pcb.Add(seg)
            seg.SetWidth(int(self.width*1e6))
            seg.SetLayer(self.layer)
            self.segments.append(seg)
            seg.SetStart(list_to_wxpoint(self.pts[i]))
            seg.SetEnd(list_to_wxpoint(self.pts[i+1]))

    def hide(self):
        for s in self.segments:
            pcb.Remove(s)
            self.segments = []

    def redraw(self):
        self.hide()
        self.render()

    def list(self):
        print([p for p in self.pts])

    def move(self, v):
        for i in range(len(self.pts)):
            self.pts[i] = [self.pts[i]+v[0], self.pts[i]+v[1]]
        self.redraw()

    def rotate(self, angle):
        for i in range(len(self.pts)):
            self.pts[i] = rot(self.pts[i], angle)
        self.redraw()

    def merge(self, new_pts):
        if isinstance(new_pts, PolyLine):
            self.pts += new_pts.pts
            new_pts.hide()
        else:
            self.pts.append(new_pts)
        self.redraw()

    def copy(self):
        cp = PolyLine(self.pcb, self.pts, layer=self.layer, width=self.width)
        return cp

    def append_arc(self, r, start_angle, end_angle, segments=6):
        da = ((end_angle - start_angle) / float(segments))
        for s in range(segments):
            sa = start_angle + (s * da)
            ea = start_angle + ((s + 1) * da)
            self.pts.append(to_cart([r, sa]))
            self.pts.append(to_cart([r, ea]))
        self.redraw()

class Mod:
    def __init__(self, pcb, m):
        self.m = m
        self.ref = self.m.GetReference()

    def get_pos(self):
        return wxpoint_to_list(self.m.GetPosition())

    def get_angle(self):
        return self.m.GetOrientation()/10.0

    def set_angle(self, a):
        self.m.SetOrientation(a*10)

    def set_pos(self, pos):
        self.move(to=pos)

    def move(self, to=None, by=None):
        pos = self.get_pos()
        new_pos = pos
        if by and not to:
            new_pos = [pos[0]+by[0], pos[1]+by[1]]
        if to and not by:
            new_pos = to
        self.m.SetPosition(list_to_wxpoint(new_pos))

    def rotate(self, angle, origin=[0, 0]):
        pos = self.get_pos()
        a = self.get_angle()
        new_pos = rot(pos, angle)
        self.move(to=new_pos)
        new_orientation = a - angle
        self.set_angle(new_orientation)

    def align(self, mod):
        self.move(to=mod.get_pos())
        self.set_angle(mod.get_angle())

    def get_value(self):
        return self.m.GetValue()

    def get_package(self):
        return self.m.GetFPID().GetLibItemName().utf8_to_wxstring()

pcb = GetBoard()

#modules M = {reference: Mod}
M = {}
for m in pcb.GetModules():
    M[m.GetReference()] = Mod(pcb, m)

#layers L = {name: number}
L = {}
for i in range(PCB_LAYER_ID_COUNT):
    L[pcb.GetLayerName(i)] = i

#nets N = {name: netcode}
N = {}
for netcode, net in pcb.GetNetsByNetcode().items():
    N[net.GetNetname()] = netcode
