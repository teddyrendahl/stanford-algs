"""
Test our minimum cut algorithm
"""
############
# Standard #
############
import os
import math
import os.path
import logging

############
# External #
############
import pytest

###########
# Package #
###########
from ..mincut import Graph, minimum_cut

test_dir = os.path.dirname(__file__)
logging.basicConfig(level=logging.INFO)

def lookup_mincut(f):
    """
    Find the answer to our minimum cut graph stored
    """
    f = f.replace('input', 'output')
    with open(f, 'r') as handle:
        min_cut = int(handle.read().split('\n',1)[0])
    return min_cut

def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for case in metafunc.cls.cases:
        idlist.append(case)
        argvalues.append(os.path.join(test_dir, case))
    metafunc.parametrize('_in', argvalues, ids=idlist, scope='class')

class TestMinCut:
    cases = [f for f in os.listdir(test_dir)
             if f.startswith('input') and  f.endswith('.txt')]

    def test_mincut(self, _in):
        graph = Graph.from_adjaceny_list(_in)
        n_int = round(len(graph) * math.log(len(graph)))
        min_cut = minimum_cut(graph, n_iterations=n_int)
        assert min_cut == lookup_mincut(_in)
