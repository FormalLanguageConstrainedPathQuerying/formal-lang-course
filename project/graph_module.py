import cfpq_data
import networkx


def get_graph_count_vertex_edges_labels(graph_name):
    graph_path = cfpq_data.download(graph_name)
    graph = cfpq_data.graph_from_csv(graph_path)
    return (
        graph.number_of_nodes(),
        graph.number_of_edges(),
        {el["label"] for (_, _, el) in graph.edges(data=True)},
    )


def build_two_cycles_graph_dot_format(
    num_vertexes_first_cycle: int,
    num_vertexes_second_cycle: int,
    labels: (str, str),
    file_path,
):
    graph = cfpq_data.labeled_two_cycles_graph(
        num_vertexes_first_cycle, num_vertexes_second_cycle, labels=labels
    )
    networkx.drawing.nx_pydot.to_pydot(graph).write_raw(file_path)
