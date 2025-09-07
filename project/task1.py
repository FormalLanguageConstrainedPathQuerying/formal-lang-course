from typing import Dict, Set, Tuple, Union

import cfpq_data
import networkx as nx
from networkx.drawing.nx_pydot import to_pydot


def get_graph_info(graph_name: str) -> Dict[str, Union[int, Set[str]]]:
    graph_path = cfpq_data.download(graph_name)
    graph = cfpq_data.graph_from_csv(graph_path)

    labels = {d["label"] for _, _, d in graph.edges(data=True)}

    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "labels": labels,
    }


def create_and_save_two_cycles_graph(
    nodes_count1: int,
    nodes_count2: int,
    labels: Tuple[str, str],
    output_path: str,
) -> None:
    if nodes_count1 < 1 or nodes_count2 < 1:
        raise ValueError("node counts must be >= 1")

    # workaround to allow self loop
    if nodes_count1 == 1 and nodes_count2 == 1:
        graph = nx.MultiDiGraph()
        graph.add_edge(0, 0, label=labels[0])
        graph.add_edge(0, 0, label=labels[1])
    elif nodes_count1 == 1:
        graph = cfpq_data.labeled_cycle_graph(nodes_count2, label=labels[1])
        graph.add_edge(0, 0, label=labels[0])
    elif nodes_count2 == 1:
        graph = cfpq_data.labeled_cycle_graph(nodes_count1, label=labels[0])
        graph.add_edge(0, 0, label=labels[1])
    else:
        # the function expects the number of nodes excluding the common node
        graph = cfpq_data.labeled_two_cycles_graph(
            n=nodes_count1 - 1, m=nodes_count2 - 1, labels=labels
        )

    pydot_graph = to_pydot(graph)
    dot_string = pydot_graph.to_string()

    with open(output_path, "w") as f:
        f.write(dot_string)
    print(f"Graph saved to {output_path}")
