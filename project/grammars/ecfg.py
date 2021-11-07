from typing import AbstractSet, Iterable

from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex

from pyformlang.cfg import CFG

from project.grammars.ecfg_production import ECFGProduction
from project.grammars.cfg_exception import CFGException

__all__ = ["ECFG"]


class ECFG:
    """
    Extended Context Free Grammar

    Attributes
    ----------
    variables: AbstractSet[Variable], default=None
        Existing variables of ECFG
    start_symbol: Variable, default=None
        Start symbol of ECFG
    productions: Iterable[ECFGProduction], default=None
        ECFG productions
    """

    def __init__(
        self,
        variables: AbstractSet[Variable] = None,
        start_symbol: Variable = None,
        productions: Iterable[ECFGProduction] = None,
    ):
        self._variables = variables or set()
        self._start_symbol = start_symbol
        self._productions = productions or set()

    @property
    def variables(self) -> AbstractSet[Variable]:
        """
        Get variables

        Returns
        -------
        variables: AbstractSet[Variable]
            self._variables field
        """
        return self._variables

    @property
    def productions(self) -> AbstractSet[ECFGProduction]:
        """
        Get productions

        Returns
        -------
        productions: Iterable[ECFGProduction]
            self._productions field
        """
        return self._productions

    @property
    def start_symbol(self) -> Variable:
        """
        Get start_symbol

        Returns
        -------
        start_symbol: Variable
            self._start_symbol field
        """
        return self._start_symbol

    def to_text(self) -> str:
        """
        Transform ECFG to string representation

        Returns
        -------
        text: str
            String representation of ECFG
        """
        return "\n".join(str(p) for p in self.productions)

    @classmethod
    def from_text(cls, text: str, start_symbol: str = Variable("S")) -> "ECFG":
        """
        Converts string representation of ECFG into ECFG class object

        Attributes
        ----------
        text: str
            String representation of ECFG
        start_symbol: str, default=Variable("S")
            Start symbol of ECFG

        Returns
        -------
        ecfg: ECFG
            ECFG object converted from string

        Raises
        ------
        CFGException
            If ECFG-text does not match required format
        """
        variables = set()
        productions = set()
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            production_objects = line.split("->")
            if len(production_objects) != 2:
                raise CFGException("There should be only one production per line.")

            head_text, body_text = production_objects
            head = Variable(head_text.strip())

            if head in variables:
                raise CFGException(
                    "There should be only one production for each variable."
                )

            variables.add(head)
            body = Regex(body_text.strip())
            productions.add(ECFGProduction(head, body))

        return ECFG(
            variables=variables,
            start_symbol=Variable(start_symbol),
            productions=productions,
        )

    @classmethod
    def from_pyformlang_cfg(cls, cfg: CFG):
        """
        Transform pyformlang CFG to ECFG object

        Attributes
        ----------
        cfg: CFG
            Pyformlang CFG object

        Returns
        -------
        ecfg: ECFG
            ECFG object
        """
        productions = dict()

        for p in cfg.productions:
            body = Regex(
                " ".join(cfg_obj.value for cfg_obj in p.body) if p.body else "$"
            )
            if p.head not in productions:
                productions[p.head] = body
            else:
                productions[p.head] = productions.get(p.head).union(body)

        ecfg_productions = [
            ECFGProduction(head, body) for head, body in productions.items()
        ]

        return ECFG(
            variables=cfg.variables,
            start_symbol=cfg.start_symbol,
            productions=ecfg_productions,
        )
