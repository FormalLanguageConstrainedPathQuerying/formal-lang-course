from typing import Tuple

import cfpq_data
import networkx


def get_graf_information_by_name(name: str):
    graph = cfpq_data.graph_from_csv(
        cfpq_data.download(name)
    )  # get path graph by name, then get graph
    return (
        graph.number_of_nodes(),
        graph.number_of_edges(),
        cfpq_data.get_sorted_labels(graph),
    )


def create_graph_by_number_vertices_in_loops_and_label_names_and_save_in_file(
    fst_nodes_count: int, snd_nodes_count: int, labels: Tuple[str, str], file_name: str
):
    graph = cfpq_data.labeled_two_cycles_graph(
        fst_nodes_count, snd_nodes_count, labels=labels
    )
    pydot_graph = networkx.drawing.nx_pydot.to_pydot(graph)
    pydot_graph.write(file_name)
