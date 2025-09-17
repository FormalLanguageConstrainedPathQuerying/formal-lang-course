from pyformlang.finite_automaton import Symbol
from project import t2_fa_utils as t2


def test_single_symbol_accepts_and_rejects():
    dfa = t2.regex_to_dfa("a")

    assert dfa.accepts([Symbol("a")])
    assert not dfa.accepts([Symbol("b")])
    assert not dfa.accepts([])


def test_union_expression():
    dfa = t2.regex_to_dfa("a|b")

    assert dfa.accepts([Symbol("a")])
    assert dfa.accepts([Symbol("b")])
    assert not dfa.accepts([Symbol("c")])


def test_concatenation_expression():
    dfa = t2.regex_to_dfa("ab")

    assert dfa.accepts([Symbol("ab")])
    assert not dfa.accepts([Symbol("a")])
    assert not dfa.accepts([Symbol("b")])


def test_kleene_star():
    dfa = t2.regex_to_dfa("a*")

    assert dfa.accepts([])
    assert dfa.accepts([Symbol("a")])
    assert dfa.accepts([Symbol("a"), Symbol("a"), Symbol("a")])
    assert not dfa.accepts([Symbol("b")])


def test_equivalent_regexes():
    dfa1 = t2.regex_to_dfa("a|b")
    dfa2 = t2.regex_to_dfa("(b|a)")

    words = [
        [],
        [Symbol("a")],
        [Symbol("b")],
        [Symbol("c")],
        [Symbol("a"), Symbol("b")],
    ]
    for w in words:
        assert dfa1.accepts(w) == dfa2.accepts(w)


def test_dfa_is_deterministic():
    dfa = t2.regex_to_dfa("a(b|c)*")

    transitions = dfa.to_dict()
    for state, edges in transitions.items():
        for symbol, targets in edges.items():
            if not isinstance(targets, set):
                targets = {targets}
            assert len(targets) == 1, f"Non-determinism in state {state} on {symbol}"
