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
from ..two_sum import find_all_two_sums, table_from_file, threaded_find_two_sum

logging.basicConfig(level=logging.INFO)
test_dir = os.path.dirname(__file__)


def lookup_answer(f):
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


class TestTwoSum:
    cases = [f for f in os.listdir(test_dir)
             if f.startswith('input') and f.endswith('.txt')]

    def test_two_sum(self, _in):
        table = table_from_file(_in)
        #ans = find_all_two_sums(table,
        #                        targets=list(range(-10000, 10001)))
        ans = threaded_find_two_sum(table)
        assert ans == lookup_answer(_in)
