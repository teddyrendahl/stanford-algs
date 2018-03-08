import copy
import itertools
from collections import namedtuple


Edge = namedtuple('Edge', ('head', 'tail', 'cost'))


class UnionFind:
    def __init__(self, nodes):
        self.nodes = nodes
        self.leaders = dict()
        self.members = dict()
        for node in nodes:
            # Keeps mapping of leaders to groups
            if str(node) not in self.leaders:
                self.leaders[str(node)] = [node]
            # Account for duplicate node ids
            else:
                self.leaders[str(node)].append(node)
            # Keeps mapping of nodes to leaders
            self.members[str(node)] = node

    def find(self, node):
        return self.members[str(node)]

    def union(self, node1, node2):
        # Find our two groups and decide which should be merged into which by
        # size of group
        (old_leader, new_leader) = sorted((self.find(node1), self.find(node2)),
                                          key = lambda x:
                                                len(self.leaders[str(x)]))
        # If these two nodes were already in the same group we are finished
        if old_leader == new_leader:
            return
        else:
            # Add the old group the new group
            old_group = self.leaders.pop(str(old_leader))
            self.leaders[str(new_leader)].extend(old_group)
            # Reassign the leaders in the old group
            for node in old_group:
                self.members[str(node)] = new_leader

def read_file(path):
    """Read a file and return a list of edges"""
    edges = list()
    with open(path, 'r') as handle:
        lines = handle.readlines()
        n_nodes = int(lines.pop(0))
        for line in lines:
            (head, tail, cost) = line.split(' ', 2)
            edges.append(Edge(int(head), int(tail), int(cost)))
    return list(range(1, n_nodes + 1)), edges


def maximum_spacing(nodes, edges, k=4):
    """Find the maximum spacing for a graph of edges with k clusters"""
    # Sort the edges by cost
    edges = sorted(edges, key=lambda x: x.cost)
    # Create our UnionFind data structure
    nodes = UnionFind(nodes)
    # While we have more groups then desired clusters
    while len(nodes.leaders) >= k:
        # Select the minimum edge and join two clusters
        min_edge = edges.pop(0)
        nodes.union(min_edge.head, min_edge.tail)
    return min_edge.cost


def read_hamming(path):
    with open(path, 'r') as handle:
        lines = handle.readlines()
    n_nodes, n_bits = lines.pop(0).split(' ', 1)
    nodes = list()
    for i, line in enumerate(lines):
        nodes.append(bytearray([int(i)
                                for i in line.split(' ', int(n_bits) - 1)]))
    return nodes

def minimum_clusters(nodes, spacing=2):
    """
    Find the minimum clusters needed to have a specific spacing
    """
    union = UnionFind(nodes)
    for i in range(1, spacing+1):
        for node in union.nodes:
            closest = hamming_possibilities(node, i)
            for partner in closest:
                try:
                    union.union(node, partner)
                except KeyError:
                    pass
    return len(union.leaders)


def flip_bit(bit):
    if bit == 1:
        return 0
    if bit == 0:
        return 1


def hamming_possibilities(node, distance):
    """Calculate all possible nodes within a hamming distance of node"""
    idxs = itertools.combinations(range(len(node)), distance)
    nodes = list()
    for shift in idxs:
        new = copy.copy(node)
        for pos in shift:
            new[pos] = flip_bit(node[pos])
        nodes.append(new)
    return nodes
