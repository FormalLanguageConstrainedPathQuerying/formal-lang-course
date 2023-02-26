import cfpq_data as cd
import networkx as nx


class GraphInfo:
    def __init__(self, number_of_nodes, number_of_edges, labels):
        self.number_of_nodes = number_of_nodes
        self.number_of_edges = number_of_edges
        self.labels = labels

    def __str__(self):
        return (
            str(self.number_of_nodes)
            + " "
            + str(self.number_of_edges)
            + " "
            + str(self.labels)
        )


def get_graph_info(name: str) -> GraphInfo:
    path = cd.download(name)
    gr = cd.graph_from_csv(path)

    unique_labels = set(
        (e[2] if (3 <= len(e)) else None) for e in gr.edges(data="label")
    )
    unique_labels.discard(None)

    return GraphInfo(gr.number_of_nodes(), gr.number_of_edges(), unique_labels)


def save_two_cycles(n: int, m: int, labels, path: str):
    gr = cd.labeled_two_cycles_graph(n=n, m=m, labels=labels)
    nx.nx_pydot.write_dot(gr, path)
