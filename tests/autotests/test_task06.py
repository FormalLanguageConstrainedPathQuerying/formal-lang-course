# This file contains test cases that you need to pass to get a grade
# You MUST NOT touch anything here except ONE block below
# You CAN modify this file IF AND ONLY IF you have found a bug and are willing to fix it
# Otherwise, please report it
import pytest
from grammars_constants import REGEXP_CFG, GRAMMARS
from rpq_template_test import rpq_cfpq_test, different_grammars_test
from cfpq_concrete_cases import CaseCFPQ, CASES_CFPQ

# Fix import statements in try block to run tests
try:
    from project.hellings_cfpq import hellings_based_cfpq
except ImportError:
    pytestmark = pytest.mark.skip("Task 6 is not ready to test!")


class TestHellingBasedCFPQ:
    @pytest.mark.parametrize("case", CASES_CFPQ)
    def test_concrete_cases(self, case: CaseCFPQ):
        case.check_answer_cfg(hellings_based_cfpq)

    @pytest.mark.parametrize("regex_str, cfg_list", REGEXP_CFG)
    def test_rpq_cfpq_hellings(self, graph, regex_str, cfg_list):
        rpq_cfpq_test(graph, regex_str, cfg_list, hellings_based_cfpq)

    @pytest.mark.parametrize("eq_grammars", GRAMMARS)
    def test_different_grammars_hellings(self, graph, eq_grammars):
        different_grammars_test(graph, eq_grammars, hellings_based_cfpq)


def test_cfg_to_weak_normal_form_exists():
    try:
        import project.hellings_cfpq

        assert "cfg_to_weak_normal_form" in dir(project.hellings_cfpq)
    except NameError:
        assert False
