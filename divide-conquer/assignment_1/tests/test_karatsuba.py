import os
import os.path
import pytest

from ..karatsuba import karatsuba


test_dir = os.path.dirname(os.path.abspath(__file__))

def parse_testcase(f):
    f = open(f, 'r')
    x, y = f.read().split('\n',1)
    return x, y

def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for case in metafunc.cls.cases:
        idlist.append(case)
        x, y = parse_testcase(os.path.join(test_dir, case))
        argvalues.append((x, y))
    metafunc.parametrize('xy', argvalues, ids=idlist, scope='class')

class TestKaratsuba:
    cases = [f for f in os.listdir(test_dir) if f.endswith('.txt')]

    def test_karatsuba(self, xy):
        x, y = xy
        assert karatsuba(x,y) == int(x)*int(y)
