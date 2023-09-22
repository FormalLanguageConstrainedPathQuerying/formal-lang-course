from pyformlang.regular_expression import Regex
from project.automaton_lib import dfa_of_regex


def test_dfa_of_regex():
    regex = Regex("aa|bb c d")
    generated_dfa = dfa_of_regex(regex)

    assert generated_dfa.is_deterministic()
    assert regex.accepts(["aa", "c", "d"]) == generated_dfa.accepts(["aa", "c", "d"])
    assert regex.accepts(["bb", "c", "d"]) == generated_dfa.accepts(["bb", "c", "d"])
    assert regex.accepts(["aa", "d"]) == generated_dfa.accepts(["aa", "d"])
    assert regex.accepts(["a", "c"]) == generated_dfa.accepts(["a", "c"])


def test_dfa_of_big_regex():
    regex = Regex("(x y|z (c*) d)|z|xx|(yy*)")
    generated_dfa = dfa_of_regex(regex)

    assert generated_dfa.is_deterministic()
    assert regex.accepts("xyzccd") == generated_dfa.accepts("xyzccd")
    assert regex.accepts(["xyzcc"]) == generated_dfa.accepts("xyzcc")
    assert regex.accepts("xyxd") == generated_dfa.accepts("xxzd")
    assert regex.accepts([]) == generated_dfa.accepts([])
    assert regex.accepts(["z"]) == generated_dfa.accepts(["z"])
    assert regex.accepts(["xx"]) == generated_dfa.accepts(["xx"])
    assert regex.accepts(["yyyyy"]) == generated_dfa.accepts(["yyyyy"])
    assert regex.accepts(["yyyy"]) == generated_dfa.accepts(["yyyy"])
