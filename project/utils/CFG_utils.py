from pyformlang.cfg import CFG, Variable


class CFGException(Exception):
    """
    Base exception for CFG utils
    """

    def __init__(self, msg):
        self.msg = msg


def read_cfg_from_file(filename: str, start_state: str):
    """
    Read and return a CFG from a file

    Parameters
    ----------
    filename: str
        Name of input file with CFG given in format:
        https://pyformlang.readthedocs.io/en/latest/modules/context_free_grammar.html#pyformlang.cfg.CFG.from_text
    start_state: str
        CFG start state

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
            return CFG.from_text(cfg_text, Variable(start_state))

    except FileNotFoundError as exc:
        raise CFGException(f"Error: File '{filename}' not found") from exc

    except ValueError as exc:
        raise CFGException(
            f"Error: CFG form in '{filename}' might be corrupted, check the correctness of CFG"
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
