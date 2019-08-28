import random

from graph import Graph, Vertex, Edge
import graphIO

def all_edges(G):
    return G.E

def all_vertices(G):
    return G.V.values()

def random_vertex(G):
    return [random.choice(G.V)]

def num_v(G):
    return len(G.V)

def pick_vertex(G, k):
    return [G.V[k]]

def out_neighbors(G, V_list):
    out = []
    for E in G.E:
        if E.u in V_list:
            out.append(E.v)
    return list(set(out)) # remove duplicates


def out_edges(G, V_list):
    out = []
    for E in G.E:
        if E.u in V_list:
            out.append(E)
    return out

def vertex_filter(G, V_list, f):
    #f is some function that evaluates to a bool
    out = []
    for V in V_list:
        if f(V):
            out.append(V)
    return out

def edge_filter(G, E_list, f):
    # f is some function that evaluates to a bool
    out = []
    for E in E_list:
        if f(E):
            out.append(E)
    return out

def broadcast(G, V_list, val):
    for V in V_list:
        V.prop = val
    return V_list

def update(G, V_list, val_list):
    i = 0
    for V, val in zip(V_list, val_list):
        V.prop = val
    return V_list

def compare_and_update(G, V_list, val_list, cmp):
    '''
    updates the list of vertices based on the comparator. If the new update exceeds the current property for the vertex, update it.
    '''
    i = 0
    updates = set()
    for V, val in zip(V_list, val_list):
        print('V=', V, 'curr=, ', V.prop[0], 'update=', val[0])
        if cmp(val, V.prop):
            V.prop = val
            updates.add(V)
    #return updated nodes only
    return list(updates)


def BFS(G):
    # All_vertices -> property(-1)
    broadcast(G, all_vertices(G), -1)

    #Random_vertex -> property(0)
    wl = broadcast(G, random_vertex(G), 0)


    #Two ways to get p_prev. Add the notion of memory (and say p_prev = max(wl).prop) or have the while keep track of iterations
    #while wl{out_neighbors(wl) -> filter(x:x.prop == -1) -> property(p_prev + 1)}
    while wl:
        p_prev = wl[0].prop
        wl = broadcast(G, vertex_filter(G, out_neighbors(G, wl),lambda v: v.prop == -1), p_prev + 1)

    print(G)

def CC(G):
    update(G, all_vertices(G), all_vertices(G))
    wl = all_edges(G)
    prev = False
    while wl:
        prev = not prev
        wl = edge_filter(G, wl, lambda e: e.u.prop != e.v.prop)
        if prev:
            #update(G, [e.u.prop for e in wl], [min(e.u.prop.prop, e.v.prop) for e in wl])
            compare_and_update(G, [e.u.prop for e in wl], [e.v.prop for e in wl], cmp = lambda u, v: u.prop < v.prop)
        else:
            #update(G, [e.u.prop for e in wl], [max(e.u.prop.prop, e.v.prop) for e in wl])
            compare_and_update(G, [e.u.prop for e in wl], [e.v.prop for e in wl], cmp = lambda u, v: u.prop > v.prop)

        update(G, all_vertices(G), [v.prop.prop for v in all_vertices(G)])
    print(G)



def SSSP_bf(G, start):
    update(G, all_vertices(G), zip([float('inf')]*len(all_vertices(G)), all_vertices(G)))
    broadcast(G, pick_vertex(G, start), (0, pick_vertex(G, start)[0]))

    wl = all_edges(G)
    cnt = len(all_vertices(G)) - 1
    while cnt > 0:
        cnt -= 1
        compare_and_update(G, [e.v for e in wl], [(e.u.prop[0] + e.w, e.u) for e in wl], cmp = lambda p1, p2: p1[0] < p2[0])

    print(G)

def SSSP_wf_sweep(G, start):
    update(G, all_vertices(G), zip([float('inf')] * len(all_vertices(G)), all_vertices(G)))
    broadcast(G, pick_vertex(G, start), (0, pick_vertex(G, start)[0]))

    wl = pick_vertex(G, start)

    i = 1
    while wl:
        print('_'*15, i, '_'*15)
        wl = compare_and_update(G, [e.v for e in out_edges(G, wl)], [(e.u.prop[0] + e.w, e.u) for e in out_edges(G, wl)], cmp = lambda p1, p2: p1[0] < p2[0])
        #print(wl)
        i += 1

    print(G)

def SSSP_nf(G, start, d):
    update(G, all_vertices(G), zip([float('inf')] * len(all_vertices(G)), all_vertices(G)))
    broadcast(G, pick_vertex(G, start), (0, pick_vertex(G, start)[0]))

    near = pick_vertex(G, start)
    far = []

    delta = d
    i = 1
    while near or far:
        while near:
            print('_'*15, i, '_'*15)
            v_update = compare_and_update(G, [e.v for e in out_edges(G, near)], [(e.u.prop[0] + e.w, e.u) for e in out_edges(G, near)], cmp = lambda p1, p2: p1[0] < p2[0])
            near = vertex_filter(G, v_update, lambda v: v.prop[0] <= delta)
            far.extend(vertex_filter(G, v_update, lambda v: v.prop[0] > delta))
            i += 1
            #print(wl)
        delta += d
        near = vertex_filter(G, far, lambda v: v.prop[0] <= delta)
        far = vertex_filter(G, far, lambda v: v.prop[0] > delta)

    print(G)

def KCore(G):
    update(G, all_vertices(G), zip([True]*num_v(G), [0]*num_v(G)))

    for level in range(num_v(G)):
        print('_'*15, 'k=', level, '_'*15)
        while True:
            updates = vertex_filter(G,
                                vertex_filter(G, all_vertices(G), lambda v: v.prop[0]),
                                lambda v: len(vertex_filter(G, out_neighbors(G, [v]), lambda u: u.prop[0])) <= level)
            broadcast(G, updates, (False, level))
            print(updates)
            if not updates:
                break

    print(G)
    



G = graphIO.readWeightedDirected('8d_sssp_nf_example.txt')
SSSP_nf(G, 1, 2)

# G = graphIO.readUnweightedUndirected('13u_2components.txt')
# CC(G)