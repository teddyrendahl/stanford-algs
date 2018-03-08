import os
import os.path
import logging

from ..clustering import read_file, maximum_spacing

import pytest


test_dir = os.path.join(os.path.dirname(__file__),
                        'cluster_cases')


def lookup_spacing(f):
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


class TestCluster:
    cases = [f for f in os.listdir(test_dir)
             if f.startswith('input') and  f.endswith('.txt')]

    def test_clustering(self, _in):
        nodes, edges = read_file(_in)
        assert maximum_spacing(nodes, edges) == lookup_spacing(_in)
