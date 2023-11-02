import pytest
from pyformlang.cfg import Variable, CFG
from pyformlang.regular_expression import Regex

from project.automaton_utils import regex_to_dfa
from project.regex import check_regex_equality
from project.cfg import cfg_to_ecfg
from project.ecfg import ecfg_to_rsm, ECFG, InvalidECFGException
from project.rsm import RSMBox


@pytest.mark.parametrize(
    "cfg, exp_ecfg_productions",
    [
        (
            """
                S -> epsilon
                """,
            {Variable("S"): Regex("$")},
        ),
        (
            """
                S -> a S b S
                S -> epsilon
                """,
            {Variable("S"): Regex("(a S b S) | $")},
        ),
        (
            """
                S -> i f ( C ) t h e n { ST } e l s e { ST }
                C -> t r u e | f a l s e
                ST -> p a s s | S
                """,
            {
                Variable("S"): Regex("i f ( C ) t h e n { ST } e l s e { ST }"),
                Variable("C"): Regex("t r u e | f a l s e"),
                Variable("ST"): Regex("p a s s | S"),
            },
        ),
    ],
)
def test_ecfg_productions(cfg, exp_ecfg_productions):
    ecfg = cfg_to_ecfg(CFG.from_text(cfg))
    ecfg_productions = ecfg.productions
    assert all(
        regex_to_dfa(production.body).is_equivalent_to(
            regex_to_dfa(exp_ecfg_productions[production.head])
        )
        for production in ecfg_productions
    ) and len(ecfg_productions) == len(exp_ecfg_productions)


@pytest.mark.parametrize(
    "text_ecfg, expected_productions",
    [
        ("""""", []),
        (
            """S -> a S b S | $""",
            {
                Variable("S"): Regex("a S b S | $"),
            },
        ),
        ("""S -> (a | b)* c""", {Variable("S"): Regex("(a | b)* c")}),
        (
            """
         S -> (a (S | $) b)*
         A -> a b c
         """,
            {
                Variable("S"): Regex("(a (S | $) b)*"),
                Variable("A"): Regex("a b c"),
            },
        ),
    ],
)
def test_read_from_text(text_ecfg, expected_productions):
    ecfg = ECFG.from_text(text_ecfg)
    assert len(ecfg.productions) == len(expected_productions) and all(
        check_regex_equality(production.body, expected_productions[production.head])
        for production in ecfg.productions
    )


@pytest.mark.parametrize(
    "text_cfg",
    [
        """S -> B -> C""",
        """A -> b B -> a""",
        """
        S -> a S b S
        A -> B ->
        """,
    ],
)
def test_more_than_one_production_on_line(text_cfg):
    with pytest.raises(InvalidECFGException):
        ECFG.from_text(text_cfg)


@pytest.mark.parametrize(
    "text_cfg",
    [
        """
        S -> B
        S -> A
        """,
        """
        A -> b
        B -> a
        A -> c""",
    ],
)
def test_more_than_one_production_for_nonterminal(text_cfg):
    with pytest.raises(InvalidECFGException):
        ECFG.from_text(text_cfg)


@pytest.mark.parametrize(
    """ecfg_text""",
    (
        """
        """,
        """
        S -> $
        """,
        """
        S -> a S b S
        B -> B B
        C -> A B C
        """,
    ),
)
def test_variables_finite_automata_regex_equality(ecfg_text):
    ecfg = ECFG.from_text(ecfg_text)
    rsm = ecfg_to_rsm(ecfg)
    act_start_variable = ecfg.start_variable
    exp_start_variable = rsm.start_variable
    exp_boxes = [
        RSMBox(production.head, regex_to_dfa(production.body))
        for production in ecfg.productions
    ]
    act_boxes = rsm.variables_finite_automata
    assert act_start_variable == exp_start_variable and act_boxes == exp_boxes
