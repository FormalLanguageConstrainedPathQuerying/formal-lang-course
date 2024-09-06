import cfpq_data
import networkx as nx


def get_info_from_graph_name(name: str):
    try:
        graph = cfpq_data.graph_from_csv(cfpq_data.download(name))
    except FileNotFoundError as e:
        raise e

    labels = cfpq_data.get_sorted_labels(graph)

    return graph.number_of_nodes(), graph.number_of_edges(), labels


def create_two_cycles_graph_and_write_to_dot(n, m, labels, output_path):
    if not output_path.endswith(".dot"):
        output_path = output_path + ".dot"

    pydot_graph = nx.drawing.nx_pydot.to_pydot(
        cfpq_data.graphs.generators.labeled_two_cycles_graph(n, m, labels=labels)
    )
    pydot_graph.write(output_path)
