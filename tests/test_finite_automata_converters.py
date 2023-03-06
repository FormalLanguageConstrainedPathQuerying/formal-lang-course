import pytest
import project  # on import will print something from __init__ file
from project.finite_automata_converters import FAConverters
from project.graph_utils import GraphUtils


def setup_module(module):
    print("finite_automata_converters setup module")


def teardown_module(module):
    print("finite_automata_converters teardown module")


def test_1_regex_to_min_dfa():
    converter = FAConverters()
    mdfa1 = converter.regex_to_min_dfa("abc|d")
    assert mdfa1.is_deterministic()
    assert mdfa1.get_number_transitions() == 2
    assert mdfa1.accepts("d")
    assert mdfa1.accepts(["abc"])
    assert mdfa1.is_equivalent_to(mdfa1.minimize())
    assert len(mdfa1.start_states) == 1
    assert len(mdfa1.final_states) == 1

    mdfa2 = converter.regex_to_min_dfa("ab(c|d)a")
    assert mdfa2.accepts(["ab", "d", "a"])
    assert mdfa2.accepts(["ab", "c", "a"])
    assert not mdfa2.accepts(["abc"])
    assert not mdfa2.accepts(["d"])
    assert mdfa2.is_equivalent_to(mdfa2.minimize())
    assert len(mdfa2.start_states) == 1
    assert len(mdfa2.final_states) == 1

    mdfa3 = converter.regex_to_min_dfa("ab(c|d)a+qwe")
    assert mdfa3.accepts(["ab", "d", "a"])
    assert mdfa3.accepts(["qwe"])
    assert mdfa3.is_equivalent_to(mdfa3.minimize())
    assert len(mdfa3.start_states) == 1
    assert len(mdfa3.final_states) == 1


def test_2_graph_to_nfa():
    graph = GraphUtils.create_two_cycle_labeled_graph(2, 3, ("a", "b"))
    nfa = FAConverters.graph_to_nfa(graph)
    assert nfa.accepts([])
    assert nfa.accepts(["a"])
    assert nfa.accepts(["b"])
    assert nfa.accepts(["a", "a", "a"])
    assert nfa.accepts(["b", "b", "b", "b"])
    assert nfa.accepts(["a", "a", "a", "b", "b", "b", "b"])
    assert not nfa.accepts(["a", "a", "a", "a", "b", "a"])
    assert nfa.accepts(["a", "a", "b", "b", "b", "b", "a"])
    assert nfa.accepts(["a", "a", "a", "a", "b", "b", "b", "b", "a"])
    assert nfa.accepts(["a", "a", "a", "a", "b", "b", "b", "b", "b"])
    assert not nfa.accepts(["a", "a", "a", "a", "b", "b", "b", "b", "b", "a"])
