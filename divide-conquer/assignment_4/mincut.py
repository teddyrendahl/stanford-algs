############
# Standard #
############
import copy
import random
import logging

############
# External #
############

###########
# Package #
###########

logger = logging.getLogger(__name__)

class Vertex:
    """
    Representation of a graph vertex

    Parameters
    ----------
    _id : int
        Identification id
    edges : list
        List of vertex ids this graph shares an edge with
    """
    def __init__(self, _id, edges):
        self.id = _id
        self.edges = edges

    @classmethod
    def from_contraction(cls, vertex1, vertex2):
        """
        Form a new vertex from the contraction of two prior ones. By default
        the lower of the two id integers is chosen for the id of the new one
        """
        logger.debug("Contracting %s and %s vertices", vertex1.id, vertex2.id)
        # Combine edges but ignore self referencing loops
        edges = [edge for vertex in [vertex1, vertex2]
                      for edge in vertex.edges
                      if edge not in [vertex1.id, vertex2.id]]
        return cls(min([vertex1.id, vertex2.id]), edges)

    def __deepcopy__(self, memo):
        return Vertex(copy.deepcopy(self.id), copy.deepcopy(self.edges))


class Edge:
    """
    Representation of an unordered graph edge

    Parameters
    ----------
    vertices : tuple
        Unordered tuple of edge endpoints
    """
    def __init__(self, vertices):
        self.vertices = vertices

    def __eq__(self, other):
        return sorted(self.vertices) == sorted(other.vertices)


class Graph:
    """
    Representation of a Graph data type

    Parameters
    ----------
    vertices : list
        List of :class:`.Vertex` objects

    Attributes
    ----------
    vertices : dict
        Dictionary of Vertex.id to :class:`.Vertex`
    """
    def __init__(self, vertices):
        self.vertices = dict((v.id, v) for v in vertices)

    @property
    def edges(self):
        """
        All of the edges in the graph as :class:`.Edge` objects
        """
        # Find all edges
        edges = [Edge((vertex.id, e)) for vertex in self.vertices.values()
                                      for e in vertex.edges]
        # Remove duplicates 
        return edges

    def contract(self, vertices):
        """
        Parameters
        ----------
        vertices : tuple
            Vertex Ids two contract into a single point
        """
        # Create our new Vertex from two contractions
        contracted = Vertex.from_contraction(self.vertices[vertices[0]],
                                             self.vertices[vertices[1]])
        # Destroy old vertices
        self.vertices.pop(vertices[0])
        self.vertices.pop(vertices[1])
        # Replace all connections to eliminated id with
        # the new contracted id
        eliminated = max(vertices)
        for vertex in self.vertices.values():
            if eliminated in vertex.edges:
                vertex.edges = [edge if edge != eliminated else contracted.id
                                for edge in vertex.edges]
        # Add our new vertex back
        self.vertices[contracted.id] = contracted

    @classmethod
    def from_adjaceny_list(cls, filename):
        """
        Create a new graph from a file

        Parameters
        ----------
        filename : str

        Returns
        -------
        graph : :class:`.Graph`
        """
        vertices = list()
        with open(filename, 'r') as f:
            for line in f.readlines():
                line_info = list(map(int, line.split()))
                vertices.append(Vertex(line_info.pop(0), line_info))
        graph = cls(vertices)
        logger.info("From file %s, found a graph "
                    "with %s vertices and %s edges",
                    filename, len(graph), len(graph.edges))
        return graph

    def __len__(self):
        return len(self.vertices)

    def __deepcopy__(self, memo):
        return Graph(copy.deepcopy(list(self.vertices.values())))


def minimum_cut(graph, n_iterations=10):
    """
    Return the minimum number of cross connections of a graph

    Parameters
    ----------
    graph : :class:`.Graph`

    n_iterations : int, optional
        Number of iterations to run random contraction algorithm
    """
    def random_contract(_graph):
        """
        Randomly contract a graph until we find the minimum number of cuts
        """
        # Create a copy of the graph so we can mess with the innards
        _graph = copy.deepcopy(_graph)
        # Make sure we are starting with a new seed
        random.seed()
        # Keep contracting until we have completed our cut
        while len(_graph) > 2:
            edge_choice = random.choice(_graph.edges)
            # Contract both edges
            _graph.contract(edge_choice.vertices)

        # Return the number of edges left by the last two nodes
        min_cut = len(_graph.edges) / 2.
        logger.info("Found a cut with %s cross-edges", min_cut)
        return min_cut

    # Run our algorithm n_iterations times, returning the smallest result
    return min([random_contract(graph) for i in range(0, n_iterations)])

