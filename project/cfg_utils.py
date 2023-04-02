from pyformlang.cfg import CFG
import pathlib


def cfg2wcnf(cfg: CFG) -> CFG:
    """
    Transform a context-free grammar into Chomsky's weak normal form

    Args:
        cfg: grammar to transform

    Returns:
        transformed grammar
    """
    wcnf = cfg.eliminate_unit_productions().remove_useless_symbols()

    productions = wcnf._get_productions_with_only_single_terminals()

    return CFG(
        start_symbol=(wcnf.start_symbol),
        productions=set(wcnf._decompose_productions(productions)),
    )


def from_file(path: pathlib.Path) -> CFG:
    """
    Reads context-free grammar from file

    Args:
        path: file path

    Returns:
        context-free grammar щиоусе
    """
    with open(path) as f:
        return CFG.from_text("".join(line for line in f))
