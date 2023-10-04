from dataclasses import dataclass
from typing import Set, List
from scipy.sparse import csr_array


@dataclass
class AutomatonBinaryMatrix:
    """
    Binary matrix representation of automaton for a label
    """

    matrix: csr_array
    starting_nodes: Set[str]
    final_nodes: Set[str]
    nodes: List[str]
    label: str
