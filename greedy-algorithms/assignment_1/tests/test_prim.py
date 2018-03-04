import os
import os.path
import logging

from ..prim import minimum_cost, read_graph

import pytest


test_dir = os.path.join(os.path.dirname(__file__),
                        'prim_cases')


def lookup_cost(f):
    f = f.replace('input', 'output')
    with open(f, 'r') as handle:
        return int(handle.readlines()[0])


def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for case in metafunc.cls.cases:
        idlist.append(case)
        argvalues.append(os.path.join(test_dir, case))
    metafunc.parametrize('_in', argvalues, ids=idlist, scope='class')


class TestPrim:
    cases = [f for f in os.listdir(test_dir)
             if f.startswith('input') and  f.endswith('.txt')]

    def test_prim(self, _in):
        nodes, edges = read_graph(_in)
        assert minimum_cost(nodes, edges) == lookup_cost(_in)
