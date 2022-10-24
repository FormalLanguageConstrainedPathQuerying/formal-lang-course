from typing import Union

from pyformlang.cfg import CFG, Variable
from typing.io import IO

__all__ = [
    "cfg_to_wcnf",
    "cfg_from_file",
]


def cfg_to_wcnf(cfg: CFG) -> CFG:
    """Converts CFG to Weak Chomsky Normal Form

    Parameters
    ----------
    cfg : CFG
        Context free grammar

    Returns
    -------
    wcnf: CFG
        Converted cfg
    """
    cleared = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    productions = cleared._decompose_productions(
        cleared._get_productions_with_only_single_terminals()
    )
    return CFG(start_symbol=cleared.start_symbol, productions=set(productions))


def cfg_from_file(
    file: Union[str, IO], start_symbol: Union[str, Variable] = Variable("S")
) -> CFG:
    """Loads CFG from file

    Parameters
    ----------
    file : Union[str, IO]
        Filename or file itself
    start_symbol : Union[str, Variable]
        The start symbol for the CFG to be loaded

    Returns
    -------
    cfg: CFG
        Loaded CFG
    """
    with open(file) as f:
        return CFG.from_text(f.read(), start_symbol=start_symbol)
