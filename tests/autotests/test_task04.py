# This file contains test cases that you need to pass to get a grade
# You MUST NOT touch anything here except ONE block below
# You CAN modify this file IF AND ONLY IF you have found a bug and are willing to fix it
# Otherwise, please report it
import random
from copy import deepcopy
import pytest
from grammars_constants import REGEXES
from helper import generate_rnd_start_and_final
from rpq_concrete_cases import CASES_RPQ, CaseRPQ

# Fix import statements in try block to run tests
try:
    from project.task3 import tensor_based_rpq
    from project.task4 import ms_bfs_based_rpq
except ImportError:
    pytestmark = pytest.mark.skip("Task 4 is not ready to test!")


@pytest.fixture(scope="class", params=range(5))
def query(request) -> str:
    return random.choice(REGEXES)


class TestRPQ:
    @pytest.mark.parametrize("case", CASES_RPQ)
    def test_concrete_cases(self, case: CaseRPQ):
        case.check_answer_regex(ms_bfs_based_rpq)

    def test(self, graph, query) -> None:
        start_nodes, final_nodes = generate_rnd_start_and_final(graph.copy())
        ms_bfs = ms_bfs_based_rpq(
            query, deepcopy(graph), deepcopy(start_nodes), deepcopy(final_nodes)
        )
        tensor = tensor_based_rpq(
            query, deepcopy(graph), deepcopy(start_nodes), deepcopy(final_nodes)
        )

        assert tensor == ms_bfs
