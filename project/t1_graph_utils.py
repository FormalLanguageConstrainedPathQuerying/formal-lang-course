import cfpq_data as cd
import networkx as nx
import dataclasses
import pydot
from typing import Tuple


@dataclasses.dataclass
class GraphMD:
    nodes_num: int
    edges_num: int
    labels: list


def get_graph_md(graph: nx.MultiDiGraph):
    unique_labels = {d["label"] for _, _, d in graph.edges(data=True) if "label" in d}
    return GraphMD(
        nodes_num=graph.number_of_nodes(),
        edges_num=graph.number_of_edges(),
        labels=list(unique_labels),
    )


# gets graph from cfpq dataset
# (naming could be more clean, but the task doesn't specify
# from where the graph should be loaded, so....)
# btw, local loader will be usefull while testing
def get_cfpq_graph_by_name(graph_name):
    path = cd.download(graph_name)
    return cd.graph_from_csv(path)


def get_cfpq_graph_md_by_name(graph_name):
    graph = get_cfpq_graph_by_name(graph_name)
    return get_graph_md(graph)


def get_graph_md_from_loc_csv(graph_name):
    graph = cd.graph_from_csv(graph_name)
    return get_graph_md(graph)


def save_nx_graph_to_dot(nx_graph: nx.MultiDiGraph, filename: str):
    dot_graph = nx.drawing.nx_pydot.to_pydot(nx_graph)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(dot_graph.to_string())  # serialize directly, no external binary


def read_graph_from_dot(filename: str) -> nx.MultiDiGraph:
    graphs = pydot.graph_from_dot_file(str(filename))
    if isinstance(graphs, list):
        graphs = graphs[0]
    return nx.MultiDiGraph(nx.nx_pydot.from_pydot(graphs))


def create_and_save_two_cycles_graph(
    cycle_sizes: Tuple[int, int], labels: Tuple[str, str], filename
):
    graph = cd.labeled_two_cycles_graph(cycle_sizes[0], cycle_sizes[1], labels=labels)
    save_nx_graph_to_dot(graph, filename)
