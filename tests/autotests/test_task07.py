# This file contains test cases that you need to pass to get a grade
# You MUST NOT touch anything here except ONE block below
# You CAN modify this file IF AND ONLY IF you have found a bug and are willing to fix it
# Otherwise, please report it
from copy import deepcopy
import pytest
from grammars_constants import REGEXP_CFG, GRAMMARS, GRAMMARS_DIFFERENT
from helper import generate_rnd_start_and_final
from rpq_template_test import rpq_cfpq_test, different_grammars_test
from cfpq_concrete_cases import CASES_CFPQ, CaseCFPQ

# Fix import statements in try block to run tests
try:
    from project.hellings_cfpq import hellings_based_cfpq
    from project.matrix_cfpq import matrix_based_cfpq
except ImportError:
    pytestmark = pytest.mark.skip("Task 7 is not ready to test!")


class TestMatrixBasedCFPQ:
    @pytest.mark.parametrize("case", CASES_CFPQ)
    def test_concrete_cases(self, case: CaseCFPQ):
        case.check_answer_cfg(matrix_based_cfpq)

    @pytest.mark.parametrize("regex_str, cfg_list", REGEXP_CFG)
    def test_rpq_cfpq_matrix(self, graph, regex_str, cfg_list) -> None:
        rpq_cfpq_test(graph, regex_str, cfg_list, matrix_based_cfpq)

    @pytest.mark.parametrize("eq_grammars", GRAMMARS)
    def test_different_grammars_matrix(self, graph, eq_grammars):
        different_grammars_test(graph, eq_grammars, matrix_based_cfpq)

    @pytest.mark.parametrize("grammar", GRAMMARS_DIFFERENT)
    def test_hellings_matrix(self, graph, grammar):
        start_nodes, final_nodes = generate_rnd_start_and_final(graph)
        hellings = hellings_based_cfpq(
            deepcopy(grammar), deepcopy(graph), start_nodes, final_nodes
        )
        matrix = matrix_based_cfpq(
            deepcopy(grammar), deepcopy(graph), start_nodes, final_nodes
        )
        assert hellings == matrix
