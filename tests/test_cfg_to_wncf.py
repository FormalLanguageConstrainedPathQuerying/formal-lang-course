import pytest
from pyformlang.cfg import CFG

from project.utils.cfg_utils import transform_cfg_to_wcnf, is_wcnf


def get_eps_generating_vars(cfg: CFG) -> set:
    return {p.head.value for p in cfg.productions if not p.body}


@pytest.fixture(
    params=[
        """
    """,
        """
    N -> A B
    """,
        """
    S -> epsilon
    S -> a S b
    S -> S S
    """,
        """
    S -> epsilon
    S -> a S b S
    """,
        """
        A -> epsilon
        B -> epsilon
        C -> epsilon
    """,
    ]
)
def cfg(request):
    return CFG.from_text(request.param)


def test_wcnf(cfg):
    wcnf = transform_cfg_to_wcnf(cfg)
    assert is_wcnf(wcnf)


@pytest.mark.parametrize(
    "cfg, exp_eps_gen_vars",
    [
        (
            """
            S -> S S | epsilon
            """,
            {"S"},
        ),
        (
            """
            S -> S S | A
            A -> B | epsilon
            B -> epsilon
            """,
            {"S"},
        ),
        (
            """
            S -> A a | S a
            A -> epsilon
            B -> epsilon
            """,
            {"A"},
        ),
    ],
)
def test_eps_generating(cfg, exp_eps_gen_vars):
    wcnf = transform_cfg_to_wcnf(CFG.from_text(cfg))
    act_eps_gen_vars = get_eps_generating_vars(wcnf)
    assert act_eps_gen_vars == exp_eps_gen_vars


@pytest.mark.parametrize(
    "cfg, contained_words",
    [
        (
            """
            S -> epsilon
            A -> a | b | c | d
            """,
            {
                True: [""],
                False: ["a", "b", "c", "d"],
            },
        ),
        (
            """
            S -> a S b S
            S -> epsilon
            """,
            {
                True: ["", "aaabbb", "abaabb", "ababab"],
                False: ["abc", "aa", "bb", "ababa"],
            },
        ),
        (
            """
            S -> i f ( C ) t h e n { ST } e l s e { ST }
            C -> t r u e | f a l s e
            ST -> p a s s | S
            """,
            {
                True: [
                    "if(true)then{pass}else{pass}",
                    "if(false)then{if(true)then{pass}else{pass}}else{pass}",
                    "if(false)then{pass}else{if(false)"
                    "then{pass}else{if(true)then{pass}else{pass}}}",
                ],
                False: ["if(true)then{pass}else{pass", "", "if()then{}else{}"],
            },
        ),
    ],
)
def test_generated_words(cfg, contained_words):
    cfg = CFG.from_text(cfg)
    wcnf = transform_cfg_to_wcnf(cfg)
    assert all(
        wcnf.contains(w) and cfg.contains(w) for w in contained_words[True]
    ) and all(
        not wcnf.contains(w) and not cfg.contains(w) for w in contained_words[False]
    )
