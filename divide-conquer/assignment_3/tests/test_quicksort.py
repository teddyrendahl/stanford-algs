import os
import pytest
import os.path
import logging

from ..quicksort import quicksort, select_first, select_last
from ..quicksort import from_file, select_threepoint_median

test_dir = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)

def find_comparisons(f):
    """
    Find the correct number inversions based on the input filename
    """
    f = f.replace('input', 'output')
    first, last, median = from_file(f)
    return first, last, median

def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for case in metafunc.cls.cases:
        idlist.append(case)
        argvalues.append(os.path.join(test_dir, case))
    metafunc.parametrize('_in', argvalues, ids=idlist, scope='class')

class TestInversions:
    cases = [f for f in os.listdir(test_dir)
             if f.startswith('input') and  f.endswith('.txt')]

    def test_quicksort_first(self, _in):
        arr = from_file(_in)
        first, last, median = find_comparisons(_in)
        assert quicksort(arr, select_first) == first

    def test_quicksort_last(self, _in):
        arr = from_file(_in)
        first, last, median = find_comparisons(_in)
        assert quicksort(arr, select_last) == last

    def test_quicksort_median(self, _in):
        arr = from_file(_in)
        first, last, median = find_comparisons(_in)
        assert quicksort(arr, select_threepoint_median) == median
