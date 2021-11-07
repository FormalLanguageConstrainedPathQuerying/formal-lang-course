from pyformlang.cfg import CFG, Variable

from project.grammars.cfg_exception import CFGException
from project.grammars.ecfg import ECFG
from project.grammars.rsm import RSM
from project.grammars.rsm_box import RSMBox

from project.utils.automata_utils import transform_regex_to_dfa


def read_cfg_from_file(filename: str, start_symbol: str):
    """
    Read and return a CFG from a file

    Parameters
    ----------
    filename: str
        Name of input file with CFG given in format:
        https://pyformlang.readthedocs.io/en/latest/modules/context_free_grammar.html#pyformlang.cfg.CFG.from_text
    start_symbol: str
        CFG start symbol

    Returns
    -------
    cfg: CFG
        CFG object read from file

    Raises
    ------
    CFGException
        If file with given filename is absent
    CFGException
        If CFG in file does not match required format
    """
    try:
        with open(filename, "r") as cfg_file:
            cfg_text = cfg_file.read()
            return CFG.from_text(cfg_text, Variable(start_symbol))

    except FileNotFoundError as exc:
        raise CFGException(f"Error: File '{filename}' not found") from exc

    except ValueError as exc:
        raise CFGException(
            f"Error: CFG form in '{filename}' might be corrupted, check the correctness of CFG"
        ) from exc


def read_ecfg_from_file(filename: str, start_symbol: str):
    """
    Read and return a ECFG from a file

    Parameters
    ----------
    filename: str
        Name of input file with ECFG given in format:
        https://pyformlang.readthedocs.io/en/latest/modules/context_free_grammar.html#pyformlang.cfg.CFG.from_text
        But productions body might be Regular Expression
    start_symbol: str
        ECFG start symbol

    Returns
    -------
    ecfg: ECFG
        ECFG object read from file

    Raises
    ------
    CFGException
        If file with given filename is absent
    CFGException
        If ECFG in file does not match required format
    """
    try:
        with open(filename, "r") as cfg_file:
            return ECFG.from_text(cfg_file.read(), start_symbol=start_symbol)

    except FileNotFoundError as exc:
        raise CFGException(f"Error: File '{filename}' not found") from exc

    except ValueError as exc:
        raise CFGException(
            f"Error: ECFG form in '{filename}' might be corrupted, check the correctness of ECFG"
        ) from exc


def transform_cfg_to_wcnf(cfg: CFG) -> CFG:
    """
    Transform given cfg into Weakened Normal Chomsky Form (WNCF)

    Parameters
    ----------
    cfg: CFG
       CFG object to transform to WNCF

    Returns
    -------
    wncf: CFG
        CFG in Weakened Normal Chomsky Form (WNCF)
    """
    wncf = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    new_productions = wncf._get_productions_with_only_single_terminals()
    new_productions = wncf._decompose_productions(new_productions)
    return CFG(start_symbol=wncf.start_symbol, productions=set(new_productions))


def transform_ecfg_to_rsm(ecfg: ECFG) -> RSM:
    """
    Transform ECFG object to a Recursive State Machine

    Attributes
    ----------
    ecfg: ECFG
        ECFG to transform

    Returns
    -------
    rsm: RSM
        RSM transformed from ECFG
    """
    boxes = [
        RSMBox(p.head, transform_regex_to_dfa(str(p.body))) for p in ecfg.productions
    ]
    return RSM(start_symbol=ecfg.start_symbol, boxes=boxes)
