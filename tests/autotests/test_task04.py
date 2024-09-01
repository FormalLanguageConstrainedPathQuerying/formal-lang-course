# This file contains test cases that you need to pass to get a grade
# You MUST NOT touch anything here except ONE block below
# You CAN modify this file IF AND ONLY IF you have found a bug and are willing to fix it
# Otherwise, please report it
import random
from copy import deepcopy
import pytest
from grammars_constants import REGEXES
from helper import generate_rnd_start_and_final, rpq_dict_to_set
from rpq_concrete_cases import CASES_RPQ, CaseRPQ

# Fix import statements in try block to run tests
try:
    from project.task2 import regex_to_dfa, graph_to_nfa
    from project.task3 import tensor_based_rpq, AdjacencyMatrixFA
    from project.task4 import ms_bfs_based_rpq
except ImportError:
    pytestmark = pytest.mark.skip("Task 4 is not ready to test!")


@pytest.fixture(scope="class", params=range(5))
def query(request) -> str:
    return random.choice(REGEXES)


class TestRPQ:
    @pytest.mark.parametrize("case", CASES_RPQ)
    def test_concrete_cases(self, case: CaseRPQ):
        fa = AdjacencyMatrixFA(
            graph_to_nfa(case.graph, case.start_nodes, case.final_nodes)
        )
        constraint_fa = AdjacencyMatrixFA(regex_to_dfa(case.regex))
        case.check_answer_automata(ms_bfs_based_rpq, fa, constraint_fa)

    def test(self, graph, query) -> None:
        start_nodes, final_nodes = generate_rnd_start_and_final(graph.copy())
        fa = AdjacencyMatrixFA(
            graph_to_nfa(deepcopy(graph), deepcopy(start_nodes), deepcopy(final_nodes))
        )
        constraint_fa = AdjacencyMatrixFA(regex_to_dfa(query))
        reachable = rpq_dict_to_set(
            ms_bfs_based_rpq(deepcopy(fa), deepcopy(constraint_fa))
        )
        ends = tensor_based_rpq(
            deepcopy(graph), deepcopy(start_nodes), deepcopy(final_nodes), query
        )

        assert set(ends) == reachable
