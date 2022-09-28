import cfpq_data
import networkx


def load_graph(name: str):
    try:
        graph_path = cfpq_data.download(name)
        return cfpq_data.graph_from_csv(graph_path)
    except FileNotFoundError as e:
        raise e


def get_graph_info(name: str):
    g = load_graph(name)

    labels = []

    for _, _, lbl in g.edges(data=True):
        labels.append(lbl["label"])

    return g.number_of_nodes(), g.number_of_edges(), labels


def create_and_save_two_cycles_graph(
    nodes_in_fst_cycle, nodes_in_snd_cycle, labels, path
):
    g = cfpq_data.labeled_two_cycles_graph(
        nodes_in_fst_cycle, nodes_in_snd_cycle, labels=labels
    )
    networkx.drawing.nx_pydot.write_dot(g, path)
