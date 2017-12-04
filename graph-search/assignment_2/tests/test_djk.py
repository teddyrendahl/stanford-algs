############
# Standard #
############
import os
import os.path
import logging

############
# External #
############

###########
# Package #
###########
from ..djk import dijkstra_shortest_path, Graph


logging.basicConfig(level=logging.INFO)
test_dir = os.path.dirname(__file__)
TEST_INDICES = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]


def lookup_min(f):
    f = f.replace('input', 'output')
    with open(f, 'r') as handle:
        for line in handle.readlines():
            return [int(i) for i in line.split(',')]


def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for case in metafunc.cls.cases:
        idlist.append(case)
        argvalues.append(os.path.join(test_dir, case))
    metafunc.parametrize('_in', argvalues, ids=idlist, scope='class')


class TestSCC:
    cases = [f for f in os.listdir(test_dir)
             if f.startswith('input') and f.endswith('.txt')]

    def test_dijkstra(self, _in):
        # Load graph
        g = Graph.from_file(_in)
        # Calculate shortest path to entire graph
        distances = dijkstra_shortest_path(g, g.nodes[1])
        # Compare results to array
        assert [distances[idx] for idx in TEST_INDICES] == lookup_min(_in)
