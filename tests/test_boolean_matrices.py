from project import (
    graph_to_nfa,
    nfa_to_boolean_matrices,
    boolean_matrices_to_nfa,
    regex_str_to_dfa,
    cross_boolean_matrices,
)
from test_graphs import all_test_graphs
from collections import namedtuple


def test_nfa_to_boolean_matrices():
    for graph in all_test_graphs:
        nfa_before = graph_to_nfa(graph.graph, graph.start_states, graph.final_states)
        matrix = nfa_to_boolean_matrices(nfa_before)
        nfa_after = boolean_matrices_to_nfa(matrix)
        assert nfa_before.is_equivalent_to(
            nfa_after
        ), f"{graph.name} failed, nfa after boolean matrix is different from before"


def test_cross_boolean_matrices():
    test_type = namedtuple(
        "test", "graph1 graph1_nfa graph2 graph2_nfa accepts rejects"
    )
    tests = []
    nfas = [regex_str_to_dfa(i.reg) for i in all_test_graphs]
    for x_ind in range(0, len(all_test_graphs)):
        for y_ind in range(x_ind + 1, len(all_test_graphs)):
            x = all_test_graphs[x_ind]
            y = all_test_graphs[y_ind]
            x_nfa = nfas[x_ind]
            y_nfa = nfas[y_ind]
            accept = []
            reject = x.rejects + y.rejects
            for i in x.accepts + y.accepts:
                if y_nfa.accepts(i) and x_nfa.accepts(i):
                    accept.append(i)
                else:
                    reject.append(i)
            if len(accept) > 0:
                tests.append(test_type(x, x_nfa, y, y_nfa, accept, reject))

    assert (
        len(tests) != 0
    ), "no one crossable pair of graphs in test graphs, add more tests"

    for test in tests:
        m1 = nfa_to_boolean_matrices(test.graph1_nfa)
        m2 = nfa_to_boolean_matrices(test.graph2_nfa)
        m3 = cross_boolean_matrices(m1, m2)
        nfa = boolean_matrices_to_nfa(m3)
        for i in test.accepts:
            assert nfa.accepts(
                i
            ), f"cross graph of {test.graph1.name}, {test.graph2.name}, {i} not accepted"
        for i in test.rejects:
            assert not nfa.accepts(
                i
            ), f"cross graph of {test.graph1.name}, {test.graph2.name}, {i} accepted"
