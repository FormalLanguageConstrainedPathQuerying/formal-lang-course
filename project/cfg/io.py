from pathlib import Path

from pyformlang.cfg import CFG, Variable


def read_from_file(path: Path, start_symbol: str = None) -> CFG:
    """Read a context free grammar from a file.
    The file contains one rule per line.
    The structure of a production is:
    head -> body1 | body2 | ... | bodyn
    where | separates the bodies.
    A variable (or non terminal) begins by a capital letter.
    A terminal begins by a non-capital character
    Terminals and Variables are separated by spaces.
    An epsilon symbol can be represented by epsilon, $, ε, ϵ or Є.
    If you want to have a variable name starting with a non-capital \
    letter or a terminal starting with a capital letter, you can \
    explicitly give the type of your symbol with "VAR:yourVariableName" \
    or "TER:yourTerminalName" (with the quotation marks). For example:
    S -> "TER:John" "VAR:d" a b

    Parameters
    ----------
    path : Path
        The path of inputted file
    start_symbol : str, optional
        The start symbol, S by default

    Returns
    -------
    cfg : CFG
        A context free grammar.
    """
    if start_symbol is None:
        start_symbol = "S"
    with open(path, "r") as file:
        text_cfg = file.read()
    return CFG.from_text(text_cfg, Variable(start_symbol))
