"""
Tests for graph data structures
"""
############
# Standard #
############
import copy

############
# External #
############
import pytest

###########
# Package #
###########
from ..mincut import Vertex, Edge, Graph

@pytest.fixture(scope='function')
def vertices():
    return (Vertex(1, [2, 3]),
            Vertex(2, [1, 3]),
            Vertex(3, [1, 2]))

def test_edge_comparison():
    e1 = Edge((1, 2))
    e2 = Edge((2, 1))
    e3 = Edge((1, 3))
    assert e1 == e2
    assert e1 != e3

def test_vertex_contraction(vertices):
    v1, v2, v3 = vertices
    contracted = Vertex.from_contraction(v1, v2)
    assert contracted.id == 1
    assert 1 not in contracted.edges
    assert sorted(contracted.edges) == [3, 3]

def test_graph_edges(vertices):
    graph = Graph(vertices)
    assert len(graph.edges) == 6

def test_graph_contraction(vertices):
    graph = Graph(vertices)
    graph.contract((2,3))
    assert len(graph) == 2
    assert 3 not in [end for edge in graph.edges
                         for end in edge.vertices]

def test_graph_copy(vertices):
    graph = Graph(vertices)
    _graph = copy.deepcopy(graph)
    _graph.vertices.pop(2)
    assert 2 in graph.vertices
    _graph.vertices[1].edges = []
    assert len(graph.vertices[1].edges) > 1
