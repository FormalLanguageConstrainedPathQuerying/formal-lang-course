import cfpq_data
from project.converter import graph_to_nfa

def test_graph_to_nfa():
    path = cfpq_data.download("bzip")
    graph = cfpq_data.graph_from_csv(path)
    nfa = graph_to_nfa(graph, set(), set())
    assert len(nfa.states) == 632
    assert len(nfa.start_states) == 632
    assert len(nfa.final_states) == 632

    nfa = graph_to_nfa(graph, set([0, 1, 2]), set([5, 6, 7, 8, 9]))
    assert len(nfa.states) == 632
    assert len(nfa.start_states) == 3
    assert len(nfa.final_states) == 5
