from pcbnew import wxPoint, GetBoard, TRACK
from math import sin, cos, radians, degrees, atan2, sqrt

PREC=2

pcb = GetBoard()

def pt2list(wxpoint):
    return [round(wxpoint.x/1e6, PREC), round(wxpoint.y/1e6, PREC)]

def list2pt(l):
    return wxPoint(int(l[0]*1e6), int(l[1]*1e6))

def ls_mods():
    mods = pcb.GetModules()
    for m in mods:
        print("{}: {} {} {}".format(m.GetReference(), m.GetValue(), pt2list(m.GetPosition()), m.GetOrientation()/10.0))

def to_polar(xy):
    rho = round(sqrt(xy[0]**2 + xy[1]**2), PREC)
    theta = round(degrees(atan2(xy[1], xy[0])), PREC)
    return [rho, theta]

def to_cart(rt):
    x = round(rt[0] * cos(radians(rt[1])), PREC)
    y = round(rt[0] * sin(radians(rt[1])), PREC)
    return [x, y]

def ls_nets():
    netcodes = pcb.GetNetsByNetcode()
    for netcode, net in netcodes.items():
        pads = net.Pads()
        print("{} {}".format(netcode, net.GetNetname()))

def ls_tracks():
    netcodes = pcb.GetNetsByNetcode()
    for netcode, net in netcodes.items():
        tracks = pcb.TracksInNet(netcode)
        print("{} {} {}".format(netcode, net.GetNetname(), [[pt2list(t.GetStart()) for t in tracks], [pt2list(t.GetEnd()) for t in tracks]]))

def get_net(n):
    if isinstance(n, int):
        nets = pcb.GetNetsByNetcode()
    if isinstance(n, basestring):
        nets = pcb.GetNetsByName()
    return nets[n]

def netcode2netname():
    #TODO:
    pass

def rot(v, a):
    ret = [round(v[0]*cos(radians(a))-v[1]*sin(radians(a)), PREC),
            round(v[0]*sin(radians(a))+v[1]*cos(radians(a)), PREC)]
    return ret

def rotate(ref, angle, origin=[0, 0]):
    module = pcb.FindModuleByReference(ref)
    pos = module.GetPosition()
    orientation = module.GetOrientation()
    new_pos = rot([pos.x/1e6, pos.y/1e6], angle)
    new_pos = wxPoint(int(new_pos[0]*1e6), int(new_pos[1]*1e6))
    new_orientation = orientation - (angle*10)
    print("{}: {}->{}, {}->{}".format(ref, pos, new_pos, orientation, new_orientation))
    module.SetPosition(new_pos)
    module.SetOrientation(new_orientation)

def move(ref, to=None, by=None):
    module = pcb.FindModuleByReference(ref)
    pos = pt2list(module.GetPosition())
    new_pos = pos
    if by and not to:
        new_pos = [pos[0]+by[0], pos[1]+by[1]]
    if to and not by:
        new_pos = to
    print("{}: {}->{}".format(ref, pos, new_pos))
    module.SetPosition(list2pt(new_pos))

def set_angle(ref, angle):
    module = pcb.FindModuleByReference(ref)
    new_orientation = (angle*10)
    module.SetOrientation(new_orientation)

def add_track(net, start, end, layer=0):
    t = TRACK(pcb)
    pcb.Add(t)
    t.SetNet(get_net(net))
    t.SetStart(list2pt(start))
    t.SetEnd(list2pt(end))
    t.SetLayer(layer)
    print("{} {} {} {}".format(net, start, end, pcb.GetLayerName(layer)))

def add_arc_track(net, r, start_angle, end_angle, segments=6, layer=0):
    da = ((end_angle - start_angle) / float(segments))
    for s in range(segments):
        sa = start_angle + (s * da)
        ea = start_angle + ((s + 1) * da)
        add_track(net, to_cart([r, sa],), to_cart([r, ea]), layer)

def get_pos(ref):
    module = pcb.FindModuleByReference(ref)
    pos = module.GetPosition()
    return pt2list(pos)
