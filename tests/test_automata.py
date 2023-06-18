from pyformlang.regular_expression import Regex
from project.my_lang.automata import *
from networkx import MultiDiGraph as Graph


def test_regex_to_dka():
    regex = Regex("(0|1)*0 0 1*")
    dka = regex_to_dka(regex)
    real = DFA()

    s0 = State(0)
    s1 = State(1)
    s2 = State(2)
    s3 = State(3)

    real.add_start_state(s0)

    real.add_final_state(s2)
    real.add_final_state(s3)

    O = Symbol("0")
    I = Symbol("1")

    real.add_transition(s0, I, s0)
    real.add_transition(s0, O, s1)
    real.add_transition(s1, I, s0)
    real.add_transition(s1, O, s2)
    real.add_transition(s2, O, s2)
    real.add_transition(s3, O, s1)
    real.add_transition(s2, I, s3)
    real.add_transition(s3, I, s3)

    assert real.is_equivalent_to(dka)
    assert True


def test_graph_to_nka():
    g = Graph()

    g.add_node(0)
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)

    g.add_edge(0, 1, label="01")
    g.add_edge(0, 0, label="00")
    g.add_edge(1, 2, label="12")
    g.add_edge(1, 3, label="13")
    g.add_edge(3, 2, label="32")

    real = NFA()

    s0 = State(0)
    s1 = State(1)
    s2 = State(2)
    s3 = State(3)

    real.add_start_state(s0)

    real.add_final_state(s2)
    real.add_final_state(s3)

    real.add_transition(s0, Symbol("01"), s1)
    real.add_transition(s0, Symbol("00"), s0)
    real.add_transition(s1, Symbol("12"), s2)
    real.add_transition(s1, Symbol("13"), s3)
    real.add_transition(s3, Symbol("32"), s2)

    nka = graph_to_nka(g, [0], [2, 3])

    assert nka.is_equivalent_to(real)
