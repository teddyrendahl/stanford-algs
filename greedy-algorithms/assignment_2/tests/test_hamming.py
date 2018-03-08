import os
import os.path
import logging

from ..clustering import read_hamming, minimum_clusters

import pytest


test_dir = os.path.join(os.path.dirname(__file__),
                        'hamming_cases')


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
        nodes = read_hamming(_in)
        assert minimum_clusters(nodes) == lookup_spacing(_in)
