import cfpq_data
import networkx


def build_and_save_graph_with_two_cicles(n1: int, n2: int, file_path: str) -> None:
    g = cfpq_data.labeled_two_cycles_graph(n1 - 1, n2 - 1)
    graph = networkx.drawing.nx_pydot.to_pydot(g)
    graph.write_raw(file_path)


def graph_info(graph_name: str) -> (int, int, set):
    graph_path = cfpq_data.download(graph_name)
    graph = cfpq_data.graph_from_csv(graph_path)

    number_of_nodes = networkx.number_of_nodes(graph)
    number_of_edges = networkx.number_of_edges(graph)
    labels = set(networkx.get_edge_attributes(graph, "label").values())

    return number_of_nodes, number_of_edges, labels


if __name__ == "__main__":
    print(graph_info("bzip"))
