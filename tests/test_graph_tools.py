import os
import random
from random import randint

import cfpq_data
import networkx as nx

from project import graph_tools, console_commands

random.seed(19)


def test_get_description() -> None:
    name = "generations"

    expected_desc = graph_tools.GraphDescription(
        name,
        129,
        273,
        cfpq_data.get_labels(cfpq_data.graph_from_dataset(name, verbose=False)),
    )

    actual_desc = graph_tools.get_description(name)

    assert (
        actual_desc.nodes == expected_desc.nodes
        and actual_desc.edges == expected_desc.edges
        and actual_desc.edge_labels == expected_desc.edge_labels
    )


def test_get_two_cycles() -> None:
    path = "tests/data/two_cycles.dot"

    if os.path.exists(path):
        os.remove(path)

    desc = {
        "first_cycle": randint(25, 49),
        "second_cycle": randint(1, 24),
        "edge_labels": ("one", "two"),
    }

    expected_graph = graph_tools.get_two_cycles(
        desc["first_cycle"], desc["second_cycle"], desc["edge_labels"]
    ).graph
    expected_graph_pydot = str(nx.drawing.nx_pydot.to_pydot(expected_graph))

    console_commands.save_graph_to_dot(path, "two_cycles")

    assert os.path.exists(path)
    with open(path, "r") as file:
        actual_graph_pydot = file.read()

        assert actual_graph_pydot == expected_graph_pydot
