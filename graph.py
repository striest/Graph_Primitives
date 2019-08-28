import math

class Vertex:
    def __init__(self, id):
        self.id = id
        self.prop = None

    def __repr__(self):
        return 'id: ' + str(self.id) + '\tprop: ' + str(self.prop) + '\n'

    def __str__(self):
        return "V" + str(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
       return self.id < other.id

    def __hash__(self):
        return hash(str(self))

class Graph:
    def __init__(self, V, E):
        self.V = V
        self.E = E

    def __repr__(self):
        return 'G:\nV = \n' +  str(self.V) + str(self.E)


class Edge:
    def __init__(self, U, V, W=float('inf')):
        self.u = U
        self.v = V
        self.w = W
    def __repr__(self):
        return str(self.u) + '--' + str(self.w) + '->' + str(self.v)

    def __eq__(self, other):
        return self.u == other.u and self.v == other.v and math.isclose(self.w, other.w, tol = 0.0000001)

    def __hash__(self):
        return hash(str(self))