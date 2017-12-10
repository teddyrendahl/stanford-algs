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
from ..median import number_stream, median_maintenance


logging.basicConfig(level=logging.INFO)
test_dir = os.path.dirname(__file__)


def lookup_median(f):
    f = f.replace('input', 'output')
    with open(f, 'r') as handle:
        for line in handle.readlines():
            return int(line)


def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for case in metafunc.cls.cases:
        idlist.append(case)
        argvalues.append(os.path.join(test_dir, case))
    metafunc.parametrize('_in', argvalues, ids=idlist, scope='class')


class TestMedian:
    cases = [f for f in os.listdir(test_dir)
             if f.startswith('input') and f.endswith('.txt')]

    def test_median(self, _in):
        stream = number_stream(_in)
        ans = median_maintenance(stream)
        assert ans == lookup_median(_in)
