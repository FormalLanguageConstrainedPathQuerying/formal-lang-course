import networkx
import pydot

from project.utils import graph_utils
from pathlib import Path


graph_env = {"test_graph": graph_utils.generate_two_cycles_graph("3", "4", "a", "b")}


def test_save_to_dot_path():
    path = graph_utils.save_to_dot(graph_env["test_graph"], "tests/data/test_graph.dot")
    assert path == Path("tests/data/test_graph.dot")


def test_save_to_dot_labels():
    graph_utils.save_to_dot(graph_env["test_graph"], "tests/data/test_labels.dot")
    pydot_graph = pydot.graph_from_dot_file("tests/data/test_labels.dot")[0]
    input_graph_env = {"input_graph": networkx.drawing.nx_pydot.from_pydot(pydot_graph)}

    info = graph_utils.get_graph_info("input_graph", env=input_graph_env)
    assert info.labels == {"a", "b"}
