from project.grapher import create_graph_with_cycles
from pydot import graph_from_dot_file
import networkx as nx
import os


def test_get_graph_data():
    name = "graph.dot"
    create_graph_with_cycles(name, 10, 20, ("a", "b", "c"))

    loaded_graph = graph_from_dot_file(name)[0]
    g = nx.drawing.nx_pydot.from_pydot(loaded_graph)

    assert len(g.nodes) == 31  # nodes count check

    cycle1 = nx.find_cycle(g, orientation="original")

    assert len(cycle1) == 11  # cycle length check

    os.remove(name)
