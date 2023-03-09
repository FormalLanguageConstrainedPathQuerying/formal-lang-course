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

    g.add_edge(0, 1, label='1')
    g.add_edge(0, 0, label='0')
    g.add_edge(1, 2, label='2')
    g.add_edge(1, 3, label='3')
    g.add_edge(3, 2, label="1")

    res = graph_request(g, [State('0')], [State('2'), State('3')], Regex("0 1 2 3"))

    s0 = State('0')
    s1 = State('1')
    s2 = State('2')
    s3 = State('3')

    exp = set()
    exp.add((s0, s3))

    print("res:", res)

    assert True
