from dataclasses import dataclass
from typing import Set


@dataclass
class GraphData:
    node_count: int
    edge_count: int
    labels: Set[str]
