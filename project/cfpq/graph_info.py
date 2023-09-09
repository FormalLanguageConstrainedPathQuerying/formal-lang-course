from dataclasses import dataclass, field


@dataclass
class GraphInfo:
    number_of_nodes: int = 0
    number_of_edges: int = 0
    unique_labels: set[str] = field(default_factory=set)
