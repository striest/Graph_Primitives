from graph import Graph, Vertex, Edge

def readUnweightedUndirected(filepath):
    fh = open(filepath, 'r')

    V = {}
    E = []

    for line in fh:
        tokens = line.split(' ')
        tail = int(tokens[0])
        head = int(tokens[1])

        if tail not in V.keys():
            V[tail] = Vertex(tail)

        if head not in V.keys():
            V[head] = Vertex(head)

        E.append(Edge(V[tail], V[head]))
        E.append(Edge(V[head], V[tail]))

    return Graph(V, E)

def readUnweightedDirected(filepath):
    fh = open(filepath, 'r')

    V = {}
    E = []

    for line in fh:
        tokens = line.split(' ')
        tail = int(tokens[0])
        head = int(tokens[1])

        if tail not in V.keys():
            V[tail] = Vertex(tail)

        if head not in V.keys():
            V[head] = Vertex(head)

        E.append(Edge(V[tail], V[head]))

    return Graph(V, E)

def readWeightedUndirected(filepath):
    fh = open(filepath, 'r')

    V = {}
    E = []

    for line in fh:
        tokens = line.split(' ')
        tail = int(tokens[0])
        head = int(tokens[1])
        weight = float(tokens[2])

        if tail not in V.keys():
            V[tail] = Vertex(tail)

        if head not in V.keys():
            V[head] = Vertex(head)

        E.append(Edge(V[tail], V[head], weight))
        E.append(Edge(V[head], V[tail], weight))

    return Graph(V, E)

def readWeightedDirected(filepath):
    fh = open(filepath, 'r')

    V = {}
    E = []

    for line in fh:
        tokens = line.split(' ')
        tail = int(tokens[0])
        head = int(tokens[1])
        weight = float(tokens[2])

        if tail not in V.keys():
            V[tail] = Vertex(tail)

        if head not in V.keys():
            V[head] = Vertex(head)

        E.append(Edge(V[tail], V[head], weight))

    return Graph(V, E)