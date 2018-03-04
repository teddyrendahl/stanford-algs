import os
import os.path
import logging

from ..scheduling import (Job, calculate_sum, schedule_by_difference,
                          schedule_by_ratio, read_jobs)

import pytest


test_dir = os.path.join(os.path.dirname(__file__),
                        'schedule_cases')


def lookup_sum(f):
    f = f.replace('input', 'output')
    with open(f, 'r') as handle:
        return [int(sm) for sm in handle.readlines()]


def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for case in metafunc.cls.cases:
        idlist.append(case)
        argvalues.append(os.path.join(test_dir, case))
    metafunc.parametrize('_in', argvalues, ids=idlist, scope='class')


class Test:
    cases = [f for f in os.listdir(test_dir)
             if f.startswith('input') and  f.endswith('.txt')]

    def test_scheduling(self, _in):
        jobs = read_jobs(_in)
        [prob_1, prob_2] = lookup_sum(_in)
        assert calculate_sum(jobs,
                             schedule_by_difference) == prob_1
        assert calculate_sum(jobs,
                             schedule_by_ratio) == prob_2
