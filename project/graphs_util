import networkx
import cfpq_data


def get_info_by_graph_name(name):
    path_to_graph = cfpq_data.download(name)
    graph = cfpq_data.graph_from_csv(path_to_graph)

    labels = []
    for e in graph.edges.data():
        labels.append(e[2]["label"])

    return graph.number_of_nodes(), graph.number_of_edges(), labels


def create_and_save_graph(
    fst_nodes_count, scnd_nodes_count, fst_label, scnd_label, path
):
    graph = cfpq_data.labeled_two_cycles_graph(
        fst_nodes_count, scnd_nodes_count, labels=(fst_label, scnd_label)
    )

    pydot_graph = networkx.drawing.nx_pydot.to_pydot(graph)
    pydot_graph.write(path)
