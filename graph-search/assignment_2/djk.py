############
# Standard #
############
import logging
from collections import namedtuple

############
# External #
############

###########
# Package #
###########

logger = logging.getLogger(__name__)
Edge = namedtuple("Edge", ('start', 'finish', 'length'))
Node = namedtuple("Node", ('name', 'edges'))


class Graph:
    """
    Graph Structure
    """
    def __init__(self, *nodes):
        self.nodes = dict()
        for node in nodes:
            self.add_node(node)

    def add_node(self, node):
        """
        Add a node to the graph
        """
        self.nodes[node.name] = node

    def find_edges(self, starts, finishes):
        """
        Find all edges starting from one group of nodes to another

        Parameters
        ----------
        starts : list of names
        finishes : list of names
        """
        def reverse_edge(edge):
            return Edge(edge.finish, edge.start, edge.length)

        edges = [edge for node in self.nodes.values() for edge in node.edges]
        # For undirected graph consider reverse
        edges += [reverse_edge(edge) for edge in edges]
        return [edge for edge in edges
                if edge.start in starts and edge.finish in finishes]

    @classmethod
    def from_file(cls, path):
        """
        Read graph structure in from file
        """
        nodes = list()
        logger.info("Reading file %s ...", path)
        with open(path, 'r') as handle:
            for line in handle.readlines():
                # Divide the name and edge structure
                name, raw_edges = line.split('\t', 1)
                name = int(name)
                edges = list()
                # Parse edge structure
                for edge in raw_edges.split('\t'):
                    if not edge.isspace():
                        finish, length = edge.split(',', 1)
                        edges.append(Edge(name, int(finish), int(length)))
                # Create node
                nodes.append(Node(name, edges))

        return cls(*nodes)

    def __eq__(self, other):
        return self.nodes == other.nodes

    def __sub__(self, other):
        return Graph(*[node for node in self.nodes.values()
                       if node not in other.nodes.values()])


def dijkstra_shortest_path(graph, s):
    """
    Find the shortest path between node s and all others in the graph

    Parameters
    ----------
    graph : Graph

    s : Node
        Starting node
    """
    # Create a new sub-area of the graph
    x = Graph(s)
    # Keep track of distances
    A = {s.name: 0}
    while x != graph:
        # Take a subsection of the graph we have not explored
        x_v = graph - x
        assert all(node not in x_v.nodes for node in x.nodes)
        assert all(node not in x.nodes for node in x_v.nodes)
        # Find edges that cross between known and unknown
        edges = graph.find_edges(x.nodes.keys(), x_v.nodes.keys())
        if not edges:
            for node in graph.nodes.values():
                for edge in node.edges:
                    if edge.start in x.nodes and edge.finish in x_v.nodes:
                        logger.error(edge)

        logger.info("Found %s edges to unexplored areas", len(edges))
        # Calculate Dijkstra's greedy criterion
        greedy = [A[edge.start] + edge.length for edge in edges]
        # Pick out the minimum based on the greedy criterion
        vw = edges[greedy.index(min(greedy))]
        assert vw.finish not in A
        assert vw.start in x.nodes and vw.finish in x_v.nodes
        logger.info("Found path of length %s to %s from %s",
                    vw.length, vw.finish, vw.start)
        # Add this new node to our graph, storing the path length
        x.add_node(graph.nodes[vw.finish])
        A[vw.finish] = A[vw.start] + vw.length
        logger.info("Total path from %s to %s is %s",
                    s.name, vw.finish, A[vw.finish])
    # Return the final distance
    return A
