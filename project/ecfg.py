from collections import defaultdict
from functools import reduce
from typing import NamedTuple, Dict, AbstractSet, Union, List

from pyformlang.cfg import Variable, CFG
from pyformlang.cfg.cfg_object import CFGObject
from pyformlang.regular_expression import Regex

__all__ = [
    "ECFG",
]

from typing.io import IO

from project import RSM


class ECFG(NamedTuple):
    """Class represents Extended Context Free Grammar

    Attributes
    ----------

    start_symbol : Variable
        Start symbol of CFG
    variables : AbstractSet[Variable]
        Set of non-terminals
    productions : Dict[Variable, Regex]
        Productions. They are represented by mapping from non-terminals to regular expressions
    """

    start_symbol: Variable
    variables: AbstractSet[Variable]
    productions: Dict[Variable, Regex]

    def to_rsm(self) -> RSM:
        """Converts ECFG to RSM

        Returns
        -------
        rsm: RSM
            Recursive state machine
        """
        return RSM(
            start_symbol=self.start_symbol,
            boxes={
                h: r.to_epsilon_nfa().to_deterministic()
                for h, r in self.productions.items()
            },
        )

    @classmethod
    def from_text(cls, text: str, start_symbol: Variable = Variable("S")):
        """Reads ECFG from text

        Parameters
        ----------
        text : str
            Text that contains extended context free grammar

        start_symbol : Variable
            Start symbol of ECFG

        Returns
        -------
        ecfg : ECFG
            Obtained context free grammar
        """
        variables = set()
        productions = dict()
        for line in text.splitlines():
            if not line.strip():
                continue
            content = [str.strip(e) for e in line.split("->")]
            assert len(content) == 2
            head, body = content
            head, body = Variable(head), Regex(body)
            assert head not in variables
            variables.add(head)
            productions[head] = body
        return cls(
            start_symbol=start_symbol,
            variables=variables,
            productions=productions,
        )

    @classmethod
    def from_file(
        cls, file: Union[str, IO], start_symbol: Union[str, Variable] = Variable("S")
    ) -> "ECFG":
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
            return ECFG.from_text(f.read(), start_symbol=start_symbol)

    @classmethod
    def from_cfg(cls, cfg: CFG) -> "ECFG":
        """Converts CFG to ECFG

        Parameters
        ----------
        cfg : CFG
            Context free grammar to be converted

        Returns
        -------
        ecfg: ECFG
            Extended context free grammar
        """
        productions = defaultdict(list)
        for p in cfg.productions:
            productions[p.head].append(p.body)
        return cls(
            start_symbol=cfg.start_symbol,
            variables=cfg.variables,
            productions={
                h: reduce(Regex.union, map(cls.concat_body, bodies))
                for h, bodies in productions.items()
            },
        )

    @staticmethod
    def concat_body(body: List[CFGObject]) -> Regex:
        """Utility function for converting body of CFG production to regex

        Parameters
        ----------
        body : List[CFGObject]
            Body of CFG production

        Returns
        -------
        regex: Regex
            Regular expression
        """
        return (
            reduce(Regex.concatenate, [Regex(o.value) for o in body])
            if body
            else Regex("")
        )
