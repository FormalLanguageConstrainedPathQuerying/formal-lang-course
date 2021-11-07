import os
from typing import AbstractSet, Iterable, Tuple, Set

import networkx as nx
from pyformlang.cfg import CFG, Variable, Production, Epsilon

__all__ = [
    "get_cfg_from_file",
    "get_cfg_from_text",
    "get_cnf_from_file",
    "get_cnf_from_text",
    "get_wcnf_from_file",
    "get_wcnf_from_text",
    "is_wcnf",
    "ECFGProduction",
    "ECFG",
    "get_ecfg_from_cfg",
    "cyk",
    "hellings",
]

from pyformlang.regular_expression import Regex


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


def get_wcnf_from_cfg(cfg: CFG) -> CFG:
    """
    Makes Context Free Grammar in Weak Chomsky Normal Form equivalent to
    given CFG.

    Parameters
    ----------
    cfg: CFG
        CFG to make WCNF

    Returns
    -------
    Tuple[CFG, CFG]:
        Context Free Grammar in Weak Chomsky Normal Form
        equivalent to CFG
    """

    wcnf = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )

    epsilon_productions = wcnf._get_productions_with_only_single_terminals()
    epsilon_productions = wcnf._decompose_productions(epsilon_productions)

    return CFG(start_symbol=wcnf.start_symbol, productions=set(epsilon_productions))


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


class ECFGProduction:
    """
    A class encapsulates a production of an Extended Context Free Grammar.

    Attributes
    ----------
    head: Variable
        The head of production
    body: Regex
        The body of production represented as Regex
    """

    def __init__(self, head: Variable, body: Regex) -> None:
        self._head = head
        self._body = body

    def __str__(self):
        return str(self.head) + " -> " + str(self.body)

    @property
    def head(self) -> Variable:
        return self._head

    @property
    def body(self) -> Regex:
        return self._body


class ECFG:
    """
    A class encapsulates an Extended Context Free Grammar.

    The Extended Context Free Grammar is Chomsky Normal Form
    by Hopcroft (without epsilon-productions) and satisfied to
    the following rules:
        - There is exactly one rule for each non-terminal
        - One line contains exactly one rule
        - Rule is non-terminal and regex over terminals
        and non-terminals accepted by pyformlang, separated by '->',
        for example: S -> a | b* S.

    Attributes
    ----------
    variables: AbstractSet[Variable], default = Set[Variable]
        Set of variables of ECFG
    start_symbol: Variable, default = Variable('S')
        Start symbol of ECFG
    productions: Iterable[ECFGProduction], default = Set[ECFGProduction]
        Collection containing productions of ECFG
    """

    def __init__(
        self,
        variables: AbstractSet[Variable] = None,
        start_symbol: Variable = None,
        productions: Iterable[ECFGProduction] = None,
    ) -> None:
        self._variables = variables or set()
        self._start_symbol = start_symbol or Variable("S")
        self._productions = productions or set()

    @property
    def variables(self) -> AbstractSet[Variable]:
        return self._variables

    @property
    def start_symbol(self) -> Variable:
        return self._start_symbol

    @property
    def productions(self) -> Iterable[ECFGProduction]:
        return self._productions

    def __str__(self) -> str:
        """
        Get a text representation of Extended Context Free Grammar.

        Returns
        -------
        str:
            Text representation of ECFG
        """

        return "\n".join(str(production) for production in self.productions)

    @classmethod
    def from_file(cls, path: str, start_symbol: str = None) -> "ECFG":
        """
        Get an Extended Context Free Grammar from file text
        representation of Context Free Grammar.

        Parameters
        ----------
        path: str
            A path to file contains text representation of CFG with rules:
            - There is exactly one rule for each non-terminal
            - One line contains exactly one rule
            - Rule is non-terminal and regex over terminals
            and non-terminals accepted by pyformlang, separated by '->',
            for example: S -> a | b* S.
        start_symbol: str, default = None
            Start symbol of CFG

        Raises
        ------
        ValueError:
           If file text is not satisfied to the rules
        MisformedRegexError
           If specified regex_str has an irregular format
        """

        with open(path) as file:
            return cls.from_text(file.read(), start_symbol=start_symbol)

    @classmethod
    def from_text(cls, cfg_text: str, start_symbol: str = None) -> "ECFG":
        """
        Get an Extended Context Free Grammar from text representation
        of Context Free Grammar.

        Parameters
        ----------
        cfg_text: str
            A text representation of CFG with rules:
            - There is exactly one rule for each non-terminal
            - One line contains exactly one rule
            - Rule is non-terminal and regex over terminals and
              non-terminals accepted by pyformlang, separated by '->',
              for example: S -> a | b * S
        start_symbol: str, default = None
            Start symbol of CFG

        Raises
        ------
        ValueError:
            If cfg_text not satisfied to the rules
        MisformedRegexError
            If specified regex_str has an irregular format
        """

        variables = set()
        productions = set()

        for line in cfg_text.splitlines():
            line = line.strip()

            if not line:
                continue

            production_text_objects = line.split("->")
            if len(production_text_objects) != 2:
                raise ValueError("Only one production per line is required")

            head_text, body_text = production_text_objects

            head = Variable(head_text.strip())
            if head in variables:
                raise ValueError("Only one production for each variable is required")
            variables.add(head)

            body = Regex(body_text.strip())

            productions.add(ECFGProduction(head, body))

        return cls(
            variables=variables, start_symbol=start_symbol, productions=productions
        )

    @classmethod
    def from_cfg(cls, cfg: CFG) -> "ECFG":
        """
        Get an Extended Context Free Grammar from Context Free Grammar.

        Parameters
        ----------
        cfg: CFG
            CFG to convert

        Returns
        -------
        ECFG:
            ECFG equivalent to given CFG
        """

        productions = dict()

        for cfg_production in cfg.productions:
            body = Regex(
                " ".join(body_object.value for body_object in cfg_production.body)
                if cfg_production.body
                else "epsilon"
            )

            if cfg_production.head not in productions:
                productions[cfg_production.head] = body
            else:
                productions[cfg_production.head] = productions.get(
                    cfg_production.head
                ).union(body)

        ecfg_productions = (
            ECFGProduction(head, body) for head, body in productions.items()
        )

        return cls(
            variables=cfg.variables,
            start_symbol=cfg.start_symbol,
            productions=ecfg_productions,
        )


def get_ecfg_from_cfg(cfg: CFG) -> ECFG:
    """
    Get an Extended Context Free Grammar from Context Free Grammar.

    Parameters
    ----------
    cfg: CFG
        CFG to convert

    Returns
    -------
    ECFG:
        ECFG equivalent to given CFG
    """

    return ECFG.from_cfg(cfg)


def cyk(word: str, cfg: CFG) -> bool:
    """
    Checks whether grammar derive the word.

    This function is applicable to any CFG.

    Parameters
    ----------
    word: str
        A word to derive in cfg
    cfg: CFG
        A CFG to derive a word

    Returns
    -------
    bool:
        Whether grammar derive the word
    """

    word_len = len(word)

    if not word_len:
        return cfg.generate_epsilon()

    cnf = cfg.to_normal_form()

    terminal_productions = [
        production for production in cnf.productions if len(production.body) == 1
    ]
    variable_productions = [
        production for production in cnf.productions if len(production.body) == 2
    ]

    matrix = [[set() for _ in range(word_len)] for _ in range(word_len)]

    for i in range(word_len):
        matrix[i][i].update(
            production.head.value
            for production in terminal_productions
            if production.body[0].value == word[i]
        )

    for length in range(1, word_len):
        for start in range(word_len - length):
            end = start + length
            for current in range(start, end):
                matrix[start][end].update(
                    production.head.value
                    for production in variable_productions
                    if production.body[0].value in matrix[start][current]
                    and production.body[1].value in matrix[current + 1][end]
                )

    return cnf.start_symbol.value in matrix[0][word_len - 1]


def hellings(cfg: CFG, graph: nx.MultiDiGraph) -> Set[Tuple[int, str, int]]:
    wcnf = get_wcnf_from_cfg(cfg)

    epsilon_heads = [
        production.head.value for production in wcnf.productions if not production.body
    ]
    terminal_productions = {
        production for production in wcnf.productions if len(production.body) == 1
    }
    variable_productions = {
        production for production in wcnf.productions if len(production.body) == 2
    }

    result = {
        (node_num, head, node_num)
        for node_num in range(graph.number_of_nodes())
        for head in epsilon_heads
    } | {
        (node_num_l, production.head.value, node_num_r)
        for node_num_l, node_num_r, edge_data in graph.edges(data=True)
        for production in terminal_productions
        if production.body[0].value == edge_data["label"]
    }

    working = result.copy()

    while working:
        node_num_l, variable_i, node_num_r = working.pop()
        pre_result = set()

        for node_num_ll, variable_j, node_num_rr in result:
            if node_num_rr == node_num_l:
                trio = {
                    (node_num_ll, production.head.value, node_num_r)
                    for production in variable_productions
                    if production.body[0].value == variable_j
                    and production.body[1].value == variable_i
                    and (node_num_ll, production.head.value, node_num_r) not in result
                }
                working |= trio
                pre_result |= trio

        result |= pre_result
        pre_result.clear()

        for node_num_ll, variable_j, node_num_rr in result:
            if node_num_ll == node_num_r:
                trio = {
                    (node_num_l, production.head.value, node_num_rr)
                    for production in variable_productions
                    if production.body[0].value == variable_i
                    and production.body[1].value == variable_j
                    and (node_num_l, production.head.value, node_num_rr) not in result
                }
                working |= trio
                pre_result |= trio

        result |= pre_result
        pre_result.clear()

    return result
