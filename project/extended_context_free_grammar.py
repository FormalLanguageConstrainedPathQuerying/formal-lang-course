from dataclasses import dataclass


@dataclass
class ECFG:
    """
    Extended context-free grammar
    Stores non-terminal and terminal symbols, productions and starting non-terminal
    """

    variables: list
    terminals: list
    productions: list
    starting_symbol: str
