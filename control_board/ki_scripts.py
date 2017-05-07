import pcbnew as p
from math import sin, cos, radians

def rot(v, a):
    ret = [round(v[0]*cos(radians(a))-v[1]*sin(radians(a)), 2),
            round(v[0]*sin(radians(a))+v[1]*cos(radians(a)), 2)]
    return ret

def rotate(ref, angle, origin=p.wxPoint(0, 0)):
    pcb = p.GetBoard()
    module = pcb.FindModuleByReference(ref)
    pos = module.GetPosition()
    orientation = module.GetOrientation()
    new_pos = rot([pos.x/1e6, pos.y/1e6], angle)
    new_pos = p.wxPoint(int(new_pos[0]*1e6), int(new_pos[1]*1e6))
    new_orientation = orientation - (angle*10)
    print("{}: {}->{}, {}->{}".format(ref, pos, new_pos, orientation, new_orientation))
    module.SetPosition(new_pos)
    module.SetOrientation(new_orientation)

def mv(ref, d):
    pcb = p.GetBoard()
    module = pcb.FindModuleByReference(ref)
    pos = module.GetPosition()
    new_pos = p.wxPoint(int(pos.x+d[0]*1e6), int(pos.y+d[1]*1e6))
    print("{}: {}->{}".format(ref, pos, new_pos))
    module.SetPosition(new_pos)

def moveTo(ref, np):
    pcb = p.GetBoard()
    module = pcb.FindModuleByReference(ref)
    pos = module.GetPosition()
    new_pos = p.wxPoint(int(np[0]*1e6), int(np[1]*1e6))
    print("{}: {}->{}".format(ref, pos, new_pos))
    module.SetPosition(new_pos)
