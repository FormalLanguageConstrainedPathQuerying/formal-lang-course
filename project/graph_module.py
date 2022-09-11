from cfpq_data import download
from cfpq_data import graph_from_csv
from cfpq_data import labeled_two_cycles_graph
from networkx.drawing.nx_pydot import to_pydot


def get_graph_count_vertex_edges_labels(graph_name):
    graph_path = download(graph_name)
    graph = graph_from_csv(graph_path)
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
    graph = labeled_two_cycles_graph(
        num_vertexes_first_cycle, num_vertexes_second_cycle, labels=labels
    )
    to_pydot(graph).write_raw(file_path)
