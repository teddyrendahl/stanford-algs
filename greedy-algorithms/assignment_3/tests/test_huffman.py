import os
import os.path
import logging

from ..huffman import from_file, huffman

import pytest


test_dir = os.path.join(os.path.dirname(__file__),
                        'huffman_cases')


def lookup_answer(f):
    f = f.replace('input', 'output')
    with open(f, 'r') as handle:
        lines = handle.readlines()
        return int(lines[0]), int(lines[1])


def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for case in metafunc.cls.cases:
        idlist.append(case)
        argvalues.append(os.path.join(test_dir, case))
    metafunc.parametrize('_in', argvalues, ids=idlist, scope='class')


class TestHuffman:
    cases = [f for f in os.listdir(test_dir)
             if f.startswith('input') and  f.endswith('.txt')]

    def test_huffman(self, _in):
        nodes = from_file(_in)
        depths = huffman(nodes)
        _max, _min = lookup_answer(_in)
        assert max(depths) == _max
        assert min(depths) == _min
