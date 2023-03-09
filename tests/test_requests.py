from project.requests import *
from pyformlang.finite_automaton import EpsilonNFA
from pyformlang.regular_expression import Regex
import pytest


def test_intersect():

    def test_intersect_regex(s1, s2):
        e1 = Regex(s1).to_epsilon_nfa()
        e2 = Regex(s2).to_epsilon_nfa()
        inter = e1.get_intersection(e2)
        mi = intersect(e1, e2)
        assert inter.is_equivalent_to(inter)

    dataset = [
        ('0', '1'),
        ('0', '0'),
        ('0*', '0'),
        ('(01)*', '0|1'),
        ('0*1*(0|1)*1', '((01)|0)*(11)*'),
        ('(01)**', '111*1'),
        ('0*1*', '(000)*|(1111)*'),
        ('0|11*0*', '1100')
    ]


    for x, y in dataset:
        test_intersect_regex(x, y)
