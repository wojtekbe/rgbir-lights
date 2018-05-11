
#distribute elements over circle
for i,r in enumerate(['C5', 'C7', 'C9', 'C11', 'C13', 'C3']):
    M[r].align(M['C5'])
    M[r].rotate(-60*i)

#outline edges
def gen_inner_edge(r, b):
    edge = PolyLine(pcb, [], layer=L['Edge.Cuts'], width=0.2)

    #add first segment
    startp = [(to_cart([r, 6])[0] - b), to_cart([r, 6])[1]]
    p = PolyLine(pcb, [startp, [startp[0], -startp[1]]])
    p.append_arc(r, -6, -60+6, segments=24)
    edge.merge(p)

    #add the rest using -60 deg rotation
    for i in range(5):
        p.rotate(-60)
        edge.merge(p)

    #close the outline
    edge.merge(startp)

    return edge

inner_edge = gen_inner_edge(46.5, 7)

mods = [M['C2'], M['C12'], M['C10'], M['C8'], M['C6']]
circle_pattern(mods, M['C4'])

mods = [M['R1'], M['R6'], M['R5'], M['R4'], M['R3']]
circle_pattern(mods, M['R2'])