############
# Standard #
############
import os
import os.path
import logging

############
# External #
############
import pytest

###########
# Package #
###########
from ..scc import find_scc

test_dir = os.path.dirname(__file__)

def lookup_scc(f):
    f = f.replace('input', 'output')
    with open(f, 'r') as handle:
        for line in handle.readlines():
            scc = [int(i) for i in line.split(',', 5)]
            return scc


def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for case in metafunc.cls.cases:
        idlist.append(case)
        argvalues.append(os.path.join(test_dir, case))
    metafunc.parametrize('_in', argvalues, ids=idlist, scope='class')


class TestSCC:
    cases = [f for f in os.listdir(test_dir)
             if f.startswith('input') and  f.endswith('.txt')]

    def test_scc(self, _in):
        assert find_scc(_in) == lookup_scc(_in)
