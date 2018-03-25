import os
import os.path
import logging

from ..knapsack import fast_knapsack as knapsack, from_file

import pytest


test_dir = os.path.dirname(__file__)


def lookup_answer(f):
    f = f.replace('input', 'output')
    with open(f, 'r') as handle:
        lines = handle.readlines()
        return int(lines[0])


def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for case in metafunc.cls.cases:
        idlist.append(case)
        argvalues.append(os.path.join(test_dir, case))
    metafunc.parametrize('_in', argvalues, ids=idlist, scope='class')


class TestKnapsack:
    cases = [f for f in os.listdir(test_dir)
             #if f.startswith('input') and  f.endswith('4_4_4.txt')]
             if f.startswith('input') and  f.endswith('txt')]

    def test_knapsack(self, _in):
        size, items = from_file(_in)
        assert knapsack(size, items) == lookup_answer(_in)
