from typing import List
from pyformlang.finite_automaton import Symbol
from project.utils.finite_automata_construct import graph_to_nfa
import cfpq_data
import pytest


@pytest.fixture()
def skos_graph():
    path = cfpq_data.download("skos")
    graph = cfpq_data.graph_from_csv(path)
    return graph


def strs_to_word(strs: List[str]) -> List[Symbol]:
    return [Symbol(s) for s in strs]


def test_all_start_and_final(skos_graph):
    nfa = graph_to_nfa(skos_graph)

    for good_input in [
        ["subPropertyOf", "subPropertyOf", "isDefinedBy"],
        ["first", "disjointWith", "isDefinedBy", "contributor"],
    ]:
        assert nfa.accepts(strs_to_word(good_input))
    for bad_input in [["type", "comment"], ["unknownSymbol"]]:
        assert not nfa.accepts(strs_to_word(bad_input))


def test_no_start_and_final(skos_graph):
    nfa = graph_to_nfa(skos_graph, [], [])
    graph = nfa.to_networkx()

    assert nfa.is_empty()
    assert graph_to_nfa(skos_graph, [], [1]).is_empty()
    assert graph_to_nfa(skos_graph, [1], []).is_empty()

    assert len(graph.nodes) == len(skos_graph.nodes)
    assert graph.edges == skos_graph.edges


def test_one_start_and_final(skos_graph):
    nfa = graph_to_nfa(skos_graph, [0], [55])

    for good_input in [
        ["isDefinedBy", "type"],
        ["subPropertyOf", "domain", "isDefinedBy", "type"],
    ]:
        assert nfa.accepts(strs_to_word(good_input))
    for bad_input in [["unknownSymbol"], ["type"], ["label"]]:
        assert not nfa.accepts(strs_to_word(bad_input))


def test_cycle_graph():
    graph = cfpq_data.graphs.labeled_cycle_graph(5, "a")
    nfa = graph_to_nfa(graph, [1], [4])

    for good_input in [["a"] * 3, ["a"] * 8, ["a"] * 13]:
        assert nfa.accepts(strs_to_word(good_input))
    for bad_input in [["a"], ["a"] * 2, ["a"] * 4, ["a"] * 5, [""], ["b"] * 3]:
        assert not nfa.accepts(strs_to_word(bad_input))
