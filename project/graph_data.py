from dataclasses import dataclass


@dataclass
class GraphData:
    node_count: int
    edge_count: int
    labels: set[str]
