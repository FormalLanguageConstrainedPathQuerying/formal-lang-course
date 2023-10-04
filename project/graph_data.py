from dataclasses import dataclass
from typing import Set


@dataclass
class GraphData:
    """
    Stores number of nodes, edges and set of all different labels
    """

    node_count: int
    edge_count: int
    labels: Set[str]
