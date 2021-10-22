import os

from pyformlang.cfg import CFG, Variable, Production, Epsilon

__all__ = [
    "get_cfg_from_file",
    "get_cfg_from_text",
    "get_cnf_from_file",
    "get_cnf_from_text",
    "get_wcnf_from_file",
    "get_wcnf_from_text",
    "is_wcnf",
]


def get_cfg_from_file(path: str, start_symbol: str = None) -> CFG:
    """
    Gets Context Free Grammar from file with given path and start symbol.

    Parameters
    ----------
    path: str
        A path to file contains text representation of CFG with rules:
        - The structure of a production is: head -> body1 | body2 | … | bodyn
        - A variable (or non terminal) begins by a capital letter
        - A terminal begins by a non-capital character
        - Terminals and Variables are separated by spaces
        - An epsilon symbol can be represented by epsilon, $, ε, ϵ or Є
    start_symbol: str, default = None
        An axiom for CFG
        If not specified, 'S' will be used

    Returns
    -------
    CFG
        Context Free Grammar equivalent to file text representation of CFG

    Raises
    ------
    OSError:
        If file does not exist or it is not ".txt" or it is empty
    ValueError:
        If file text not satisfied to the rules
    """

    _check_path(path)

    with open(path, "r") as file:
        cfg_text = file.read()

    return get_cfg_from_text(cfg_text, start_symbol)


def get_cfg_from_text(cfg_text: str, start_symbol: str = None) -> CFG:
    """
    Gets Context Free Grammar equivalent to text representation of CFG.

    Parameters
    ----------
    cfg_text: str
        Text representation of CFG with rules:
        - The structure of a production is: head -> body1 | body2 | … | bodyn
        - A variable (or non terminal) begins by a capital letter
        - A terminal begins by a non-capital character
        - Terminals and Variables are separated by spaces
        - An epsilon symbol can be represented by epsilon, $, ε, ϵ or Є
    start_symbol: str, default = None
        An axiom for CFG
        If not specified, 'S' will be used

    Returns
    -------
    CFG:
        Context Free Grammar equivalent to text representation of CFG

    Raises
    ------
    ValueError:
        If text not satisfied to the rules
    """

    if start_symbol is None:
        start_symbol = "S"
    axiom = Variable(start_symbol)

    cfg = CFG.from_text(cfg_text, axiom)

    return cfg


def get_cnf_from_file(path: str, start_symbol: str = None) -> (CFG, CFG):
    """
    Makes Context Free Grammars (with epsilon by Chomsky, no epsilon by Hopcroft) in Chomsky Normal Form
    equivalent to file text representation of CFG. Both versions are equal if CNF doesn't contain epsilon productions.

    The Chomsky Normal Form is a more strict case of the Weak Chomsky Normal Form,
    which can be weakened to it through product changes.

    Parameters
    ----------
    path: str
        A path to file contains text representation of CFG with rules:
        - The structure of a production is: head -> body1 | body2 | … | bodyn
        - A variable (or non terminal) begins by a capital letter
        - A terminal begins by a non-capital character
        - Terminals and Variables are separated by spaces
        - An epsilon symbol can be represented by epsilon, $, ε, ϵ or Є
    start_symbol: str, default = None
        An axiom for CFG
        If not specified, 'S' will be used

    Returns
    -------
    Tuple[CFG, CFG]:
        Context Free Grammars (with epsilon by Chomsky, no epsilon by Hopcroft) in Chomsky Normal Form
        equivalent to file text representation of CFG

    Raises
    ------
    OSError:
        If file does not exist or it is not ".txt" or it is empty
    ValueError:
        If file text not satisfied to the rules
    """

    _check_path(path)

    with open(path, "r") as file:
        cfg_text = file.read()

    return get_cnf_from_text(cfg_text, start_symbol)


def get_cnf_from_text(cfg_text: str, start_symbol: str = None) -> (CFG, CFG):
    """
    Makes Context Free Grammars (with epsilon by Chomsky, no epsilon by Hopcroft) in Chomsky Normal Form
    equivalent to text representation of CFG. Both versions are equal if CNF doesn't contain epsilon productions.

    The Chomsky Normal Form is a more strict case of the Weak Chomsky Normal Form,
    which can be weakened to it through product changes.

    Parameters
    ----------
    cfg_text: str
        Text representation of CFG with rules:
        - The structure of a production is: head -> body1 | body2 | … | bodyn
        - A variable (or non terminal) begins by a capital letter
        - A terminal begins by a non-capital character
        - Terminals and Variables are separated by spaces
        - An epsilon symbol can be represented by epsilon, $, ε, ϵ or Є
    start_symbol: str, default = None
        An axiom for CFG
        If not specified, 'S' will be used

    Returns
    -------
    Tuple[CFG, CFG]:
        Context Free Grammars (with epsilon by Chomsky, no epsilon by Hopcroft) in Chomsky Normal Form
        equivalent to text representation of CFG

    Raises
    ------
    ValueError:
        If text not satisfied to the rules
    """

    if start_symbol is None:
        start_symbol = "S"
    axiom = Variable(start_symbol)

    cfg = CFG.from_text(cfg_text, axiom)

    hopcroft_cnf = cfg.to_normal_form()
    productions = set(hopcroft_cnf.productions)
    chomsky_cnf = hopcroft_cnf

    if cfg.generate_epsilon():
        productions.add(Production(axiom, [Epsilon()]))

        chomsky_cnf = CFG(start_symbol=axiom, productions=set(productions))

    return chomsky_cnf, hopcroft_cnf


def get_wcnf_from_file(path: str, start_symbol: str = None) -> CFG:
    """
    Makes Context Free Grammar in Weak Chomsky Normal Form equivalent to
    file text representation of CFG.

    Parameters
    ----------
    path: str
        A path to file contains text representation of CFG with rules:
        - The structure of a production is: head -> body1 | body2 | … | bodyn
        - A variable (or non terminal) begins by a capital letter
        - A terminal begins by a non-capital character
        - Terminals and Variables are separated by spaces
        - An epsilon symbol can be represented by epsilon, $, ε, ϵ or Є
    start_symbol: str, default = None
        An axiom for CFG
        If not specified, 'S' will be used

    Returns
    -------
    CFG:
        Context Free Grammar in Weak Chomsky Normal Form
        equivalent to file text representation of CFG

    Raises
    ------
    OSError:
        If file does not exist or it is not ".txt" or it is empty
    ValueError:
        If file text not satisfied to the rules
    """

    _check_path(path)

    with open(path, "r") as file:
        cfg_text = file.read()

    return get_wcnf_from_text(cfg_text, start_symbol)


def get_wcnf_from_text(cfg_text: str, start_symbol: str = None) -> CFG:
    """
    Makes Context Free Grammar in Weak Chomsky Normal Form equivalent to
    text representation of CFG.

    Parameters
    ----------
    cfg_text: str
        Text representation of CFG with rules:
        - The structure of a production is: head -> body1 | body2 | … | bodyn
        - A variable (or non terminal) begins by a capital letter
        - A terminal begins by a non-capital character
        - Terminals and Variables are separated by spaces
        - An epsilon symbol can be represented by epsilon, $, ε, ϵ or Є
    start_symbol: str, default = None
        An axiom for CFG
        If not specified, 'S' will be used

    Returns
    -------
    Tuple[CFG, CFG]:
     Context Free Grammar in Weak Chomsky Normal Form
     equivalent to text representation of CFG

    Raises
    ------
    ValueError:
        If text not satisfied to the rules
    """

    if start_symbol is None:
        start_symbol = "S"
    axiom = Variable(start_symbol)

    cfg = CFG.from_text(cfg_text, axiom)

    wcnf = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )

    epsilon_productions = wcnf._get_productions_with_only_single_terminals()
    epsilon_productions = wcnf._decompose_productions(epsilon_productions)

    return CFG(start_symbol=wcnf.start_symbol, productions=set(epsilon_productions))


def _check_path(path: str) -> None:
    """
    Checks whether path is representing a non-empty file with ".txt" extension.

    Parameters
    ----------
    path: str
        A path to file contains text representation of CFG

    Returns
    -------
    None

    Raises
    ------
    OSError:
         If file does not exist or it is not ".txt" or it is empty
    """

    if not os.path.exists(path):
        raise OSError("Wrong file path specified: file is not exists")
    if not path.endswith(".txt"):
        raise OSError("Wrong file path specified: *.txt is required")
    if os.path.getsize(path) == 0:
        raise OSError("Wrong file path specified: file is empty")


def is_wcnf(acnf: CFG, cfg: CFG) -> bool:
    """
    Check whether given any Chomsky Normal Form derived from given Context Free Grammar is Weak.
    It is also check whether every reachable epsilon production from given Context Free Grammar
    is present in any Chomsky Normal Form.

    The rules of Weak Chomsky Normal Form are:
    - A -> B C, where A, B, C in Variables;
    - A -> a, where A in Variables, a in Terminals;
    - A -> epsilon, where A in Variables.

    Parameters
    ----------
    acnf: CFG
        Any Normal Form to check whether it is Weak
    cfg: CFG
        Context Free Grammar from which any Chomsky Normal Form is derived

    Returns
    -------
    Bool:
        Result of checking
    """

    for production in acnf.productions:
        body = production.body

        # Check the rules
        if not (
            (len(body) <= 2 and all(map(lambda x: x in acnf.variables, body)))
            or (len(body) == 1 and body[0] in acnf.terminals)
            or (not body)
        ) or not __check_epsilon_productions(
            acnf.variables, acnf.productions, cfg.productions
        ):
            return False

    return True


def __check_epsilon_productions(cnf_variables, cnf_productions, cfg_productions):
    """
    Check whether all reachable epsilon productions from
    Context Free Grammar are present in Chomsky Normal Form productions.
    """

    cfg_epsilon_productions = set(
        filter(
            lambda prod: prod.head in cnf_variables and not prod.body,
            cfg_productions,
        )
    )

    cnf_epsilon_productions = set(filter(lambda prod: not prod.body, cnf_productions))

    for epsilon_production in cfg_epsilon_productions:
        if epsilon_production not in cnf_epsilon_productions:
            return False

    return True
