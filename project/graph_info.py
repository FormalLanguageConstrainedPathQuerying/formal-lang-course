from dataclasses import dataclass


@dataclass
class GraphInfo:
    number_of_nodes: int
    number_of_edges: int
    edge_labels: set

    def __repr__(self):
        return (
            f"Number of nodes: {self.number_of_nodes}\n"
            f"Number of edges: {self.number_of_edges}\n"
            f"Labels of edges : {self.edge_labels}\n"
        )
