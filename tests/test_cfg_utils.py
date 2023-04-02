from project.cfg_utils import cfg2wcnf, from_file
from pyformlang.cfg import CFG


def test_cfg2wcnf():
    sensitive = """
    S -> 012
    S -> 0TS2
    T0 -> 0T
    T1 -> 11
    """

    gram = CFG.from_text(sensitive)
    wcnf = cfg2wcnf(gram)

    assert wcnf.to_text() == CFG.from_text("S -> 012\nS -> 0TS2").to_text()


def test_from_file():
    brackets = """
    S -> (S)S
    S -> S(S)
    S -> $
    """

    with open("/tmp/brackets.txt", "w") as f:
        f.write(brackets)

    assert from_file("/tmp/brackets.txt").to_text() == CFG.from_text(brackets).to_text()
