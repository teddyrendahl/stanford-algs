import os
import os.path
import pytest

from ..inversion import from_file, find_inversions

test_dir = os.path.dirname(os.path.abspath(__file__))

def find_count(f):
    """
    Find the correct number inversions based on the input filename
    """
    f = f.replace('input', 'output')
    with open(f, 'r') as handle:
        inv_count = int(handle.read().split('\n',1)[0])
    return inv_count

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

    def test_inversion_count(self, _in):
        assert find_inversions(from_file(_in)) == find_count(_in) 
