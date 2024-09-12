from project.task2 import regex_to_dfa


def test_regex_to_dfa():
    dfa = regex_to_dfa("a|b|c*")

    assert dfa.accepts("a")
    assert not dfa.accepts("aa")
    assert dfa.accepts("ccc")
    assert dfa.accepts("")
