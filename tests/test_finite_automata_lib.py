from project import finite_automata_lib, graph_lib
from cfpq_data import labeled_two_cycles_graph


def test_regex_to_dfa():
    dfa = finite_automata_lib.regex_to_dfa("c*a*t*|s+")
    assert dfa.accepts("")
    assert dfa.accepts("a")
    assert dfa.accepts("cat")
    assert dfa.accepts("s")
    assert not dfa.accepts("cats")


def test_graph_to_nfa():
    graph_from_dataset = graph_lib.get_graph_by_name("pizza")
    nfa_from_dataset_graph = finite_automata_lib.graph_to_nfa(
        graph_from_dataset, {54, 366}, {}
    )

    lab_two_cycles_graph = labeled_two_cycles_graph([0, 1, 2, 3, 4, 5], [5, 6, 7])
    nfa_from_two_cycle_graph = finite_automata_lib.graph_to_nfa(
        lab_two_cycles_graph, {}, {5, 6, 7}
    )

    assert nfa_from_dataset_graph.start_states == {54, 366}
    assert nfa_from_dataset_graph.final_states == set(graph_from_dataset.nodes)
    assert nfa_from_two_cycle_graph.start_states == set(lab_two_cycles_graph.nodes)
    assert nfa_from_two_cycle_graph.final_states == {5, 6, 7}
