import random
from collections import namedtuple


Edge = namedtuple('Edge', ('head', 'tail', 'cost'))


def read_graph(path):
    with open(path, 'r') as handle:
        lines = handle.readlines()
    nodes = list(range(1, int(lines[0].split(' ')[0]) + 1))
    edges = list()
    for line in lines[1:]:
        (head, tail, cost) = line.split(' ', 2)
        edges.append(Edge(int(head), int(tail), int(cost)))
    return nodes, edges


def minimum_cost(V, edges):
    X = {random.choice(V)}
    V = set(V)
    T = set()
    while X != V:
        # Find crossing edges
        choices = [edge for edge in edges
                   if (edge.head in X) ^ (edge.tail in X)]
        # Find that with minimum cost
        e = min(choices, key=lambda x: x.cost)
        # Add the edge to our M.S.T
        T.add(e)
        # Add the node to the cut
        for node in (e.head, e.tail):
            X.add(node)
    # Calculate the total cost
    return sum([edge.cost for edge in T])
