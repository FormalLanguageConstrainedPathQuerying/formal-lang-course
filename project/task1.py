import cfpq_data
import networkx as nx


def get_graph_info(name: str) -> tuple[int, int, set]:
    path = cfpq_data.download(name)
    graph = cfpq_data.graph_from_csv(path)

    edges = graph.number_of_edges()
    vertices = graph.number_of_nodes()

    edge_labels = []
    for u, v, e in graph.edges(data=True):
        edge_labels.append(e["label"])

    return edges, vertices, set(edge_labels)


def make_and_save_dot(
    len1: int, len2: int, save_path: str, labels: tuple[str, str]
) -> None:
    graph = cfpq_data.labeled_two_cycles_graph(len1, len2, labels=labels)
    data = nx.drawing.nx_pydot.to_pydot(graph)
    data.write_raw(save_path)


if __name__ == "__main__":
    print("HI")
    print(get_graph_info("bzip"))
