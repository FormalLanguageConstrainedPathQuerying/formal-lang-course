import inspect
import json
import pathlib

import cfpq_data
import networkx as nx
import pydot
import pytest

from project.rpq import rpq


def dot_to_graph(content: str):
    return nx.drawing.nx_pydot.from_pydot(pydot.graph_from_dot_data(content)[0])


def two_cycle_graph():
    return cfpq_data.labeled_two_cycles_graph(3, 2, labels=("a", "b"))


def empty_graph():
    return nx.empty_graph(create_using=nx.MultiDiGraph)


def linear_graph():
    graph = nx.MultiDiGraph()
    graph.add_edges_from(
        [(0, 1, {"label": "a"}), (1, 2, {"label": "b"}), (2, 3, {"label": "b"})]
    )

    return graph


graphs = {
    "two_cycle_graph": two_cycle_graph,
    "empty_graph": empty_graph,
    "linear_graph": linear_graph,
}


def construct_touple(data):
    expected = set()
    for pair in data["expected"]:
        expected.add((pair[0], pair[1]))

    return (
        graphs[data["graph"]](),
        data["query"],
        set(start_node for start_node in data["starts"]),
        set(start_node for start_node in data["finishes"]),
        expected,
    )


def get_data(test_name):
    with pathlib.Path(inspect.stack()[1].filename) as f:
        parent = f.parent
    with open(parent / "test_rpq.json") as f:
        test_datas = json.load(f)

    return [construct_touple(cur_block) for cur_block in test_datas[test_name]]


@pytest.mark.parametrize(
    "graph, query, start_nodes, final_nodes, expected_rpq", get_data("rpq")
)
def test_two_cycle_graph(graph, query, start_nodes, final_nodes, expected_rpq):
    actual_rpq = rpq(graph, query, start_nodes, final_nodes)
    assert actual_rpq == expected_rpq
