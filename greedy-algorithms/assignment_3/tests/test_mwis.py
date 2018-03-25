import os
import os.path
import logging

from ..mwis import from_file, mwis

import pytest


test_dir = os.path.join(os.path.dirname(__file__),
                        'mwis_cases')


def lookup_answer(f):
    f = f.replace('input', 'output')
    with open(f, 'r') as handle:
        return str(handle.readlines()[0].rstrip('\n'))


def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for case in metafunc.cls.cases:
        idlist.append(case)
        argvalues.append(os.path.join(test_dir, case))
    metafunc.parametrize('_in', argvalues, ids=idlist, scope='class')


class TestMWIS:
    cases = [f for f in os.listdir(test_dir)
             if f.startswith('input') and  f.endswith('.txt')]

    def test_mwis(self, _in):
        assert mwis(from_file(_in)) == lookup_answer(_in)
