from pathlib import Path

import networkx
from pyformlang.regular_expression import Regex
from scipy import sparse

from project.automata.bool_matrix import BoolMatrix
from project.automata.builders import build_minimal_dfa, build_nfa


class TestsForBoolMatrix:
    def test_init(self):
        dfa = build_minimal_dfa(Regex("a.b.c.d|b.c|(d.e)*"))
        bm = BoolMatrix(dfa)

        assert len(bm.states) == len(dfa.states)
        assert bm.states.keys() == dfa.states
        assert bm.matrices.keys() == dfa.symbols

        assert all(
            bm.states[start_state] in bm.start_states
            for start_state in dfa.start_states
        )
        assert all(
            bm.states[final_state] in bm.final_states
            for final_state in dfa.final_states
        )

    def test_to_nfa(self):
        dfa = build_minimal_dfa(Regex("a.b|c|(d.e)*"))
        bm = BoolMatrix(dfa)

        assert bm.to_nfa().is_equivalent_to(dfa)

    def test_intersect(self):
        bm1 = BoolMatrix(build_minimal_dfa(Regex("(a|b|c)*")))
        bm2 = BoolMatrix(build_minimal_dfa(Regex("(b|c|d)*")))
        expected_automata = build_minimal_dfa(Regex("(b|c)*"))

        bm_intersected = bm1.intersect(bm2)
        nfa = bm_intersected.to_nfa()

        assert nfa.is_equivalent_to(expected_automata)

    def test_transitive_closure(self):
        graph = networkx.nx_pydot.read_dot(Path("./resources/dfa3.dot"))

        nfa = build_nfa(graph, start_states={"0"}, final_states={"2"})
        bm = BoolMatrix(nfa)
        trc = bm.transitive_closure().toarray()

        expected = {
            "0": {"0": False, "1": True, "2": True, "3": True, "4": True},
            "1": {"0": False, "1": False, "2": True, "3": True, "4": True},
            "2": {"0": False, "1": False, "2": False, "3": True, "4": True},
            "3": {"0": False, "1": False, "2": False, "3": True, "4": False},
            "4": {"0": False, "1": False, "2": False, "3": False, "4": False},
        }

        assert all(
            trc[bm.states[start_state]][bm.states[final_state]] == result
            for start_state, row in expected.items()
            for final_state, result in row.items()
        )

    def test_direct_sum(self):
        bm1 = BoolMatrix(build_minimal_dfa(Regex("a.b|c*")))
        bm2 = BoolMatrix(build_minimal_dfa(Regex("(b)*")))

        summed_bm = bm1.direct_sum(bm2)

        assert len(summed_bm.states) == len(bm1.states) + len(bm2.states)
        assert (
            summed_bm.matrices["b"].toarray().tolist()
            == sparse.bmat(
                [
                    [bm1.matrices["b"], None],
                    [None, bm2.matrices["b"]],
                ]
            )
            .toarray()
            .tolist()
        )

    def test_build_front(self):
        graph = networkx.nx_pydot.read_dot(Path("./resources/dfa4.dot"))
        bm1 = BoolMatrix(
            build_nfa(graph, start_states={"2", "0"}, final_states={"0", "1", "2"})
        )
        dfa = build_minimal_dfa(Regex("a.b|a.c"))
        bm2 = BoolMatrix(dfa)

        actual = bm1.build_front_matrix(bm2, False).toarray()
        for i in range(len(actual)):
            for j in range(len(actual[i])):
                if j >= len(bm2.states):
                    assert bool(actual[i, j]) == (
                        j - len(bm2.states) in bm1.start_states
                    )
                else:
                    assert bool(actual[i, j]) == (i % len(bm2.states) == j)

    def test_validate_front(self):
        graph = networkx.nx_pydot.read_dot(Path("./resources/dfa2.dot"))
        bm1 = BoolMatrix(
            build_nfa(graph, start_states={"0"}, final_states={"0", "1", "2"})
        )
        dfa = build_minimal_dfa(Regex("a|c|b*|d"))
        bm2 = BoolMatrix(dfa)

        front = bm1.build_front_matrix(bm2, False)
        assert (
            front.toarray().tolist()
            == BoolMatrix.validate_front(front, len(bm2.states)).toarray().tolist()
        )
