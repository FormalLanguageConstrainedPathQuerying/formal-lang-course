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


def test_request():
    g = MultiDiGraph()

    g.add_node(0)
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)

    g.add_edge(0, 1, label='a')
    g.add_edge(0, 0, label='e')
    g.add_edge(1, 2, label='b')
    g.add_edge(2, 3, label='c')
    g.add_edge(3, 1, label="g")

    def check(str, set):
        assert graph_request(g, [0], [2, 3], Regex(str)) == set

    check('a b', {(0, 2)})
    check('a b c', {(0, 3)})
    check('a b c*', {(0, 2), (0, 3)})
    check('a b d*', {(0, 2)})
    check('a', set())
    check('a b d', set())
    check('a b c (g b c)*', {(0, 3)})
    check('e a b c', {(0, 3)})
    check('e* a b c', {(0, 3)})
    check('a (b c g)* b c', {(0, 3)})
    check('a (b c g)* (b c | b)', {(0, 2), (0, 3)})
    check('a (b c g) (b c | b)', {(0, 2), (0, 3)})
    check('a (b c | b)', {(0, 2), (0, 3)})
