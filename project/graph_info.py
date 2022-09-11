from dataclasses import dataclass


@dataclass
class GraphInfo:
    n_nodes: int
    n_edges: int
    edge_labels: set

    def __repr__(self):
        return (
            f"Number of nodes: {self.n_nodes}\n"
            f"Number of edges: {self.n_edges}\n"
            f"Labels of edges : {self.edge_labels}\n"
        )
