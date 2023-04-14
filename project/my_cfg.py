from pyformlang.cfg import Variable, Terminal, CFG
from pyformlang.regular_expression import Regex


class ECFG:
    """
    Class of extended context-free grammar
    """

    def __init__(
        self,
        s_s: Variable,
        vs: set[Variable],
        prs: dict[Variable, Regex],
        ts: set[Terminal] = None,
    ):
        """
        Constructor
        :param s_s: start symbol
        :param vs: variables
        :param prs: productions
        :param ts: terminals
        """
        self.s_s: Variable = s_s
        self.vs: set[Variable] = vs
        self.ps: dict[Variable, Regex] = prs
        self.ts: set[Terminal] = set() if ts is None else None

    @classmethod
    def convert_cfg(cls, cfg: CFG):
        """
        Convert context-free grammar to extended version
        :param cfg: original grammar
        :return: extended context-free grammar
        """
        productions: dict = {}
        for item in cfg.productions:
            regexStr = (
                "" if len(item.body) == 0 else " ".join(s.value for s in item.body)
            )
            regex = Regex(regexStr)
            productions[item.head] = (
                productions[item.head].union(regex)
                if item.head in productions
                else regex
            )
        return cls(
            cfg.start_symbol, set(cfg.variables), productions, set(cfg.terminals)
        )

    @classmethod
    def convert_text(cls, text: str, start_symbol=Variable("S")):
        """
        Parse from text extended context-free grammar
        :param text: text with ECFG
        :param start_symbol: Grammar start symbol
        :return: extended context-free grammar
        """
        variables: set[Variable] = set()
        productions: dict[Variable, Regex] = dict()

        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            product = line.split("->")
            if len(product) != 2:
                raise Exception(f"Parse in incorrect in line: {line}")

            root = Variable(product[0].strip())
            if root in variables:
                raise Exception(f"Definition of {root} is incorrect on parse line: {line}")

            variables.add(root)
            regex = Regex(product[1].strip())
            productions[root] = regex
        return cls(start_symbol, variables, productions)
