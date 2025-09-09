import os
import tempfile
import pydot
from project.simple_graph_funcs import get_graph_info, create_and_save_two_cycled_graph


def test_get_graph_info():
    nodes, edges, labels = get_graph_info("wc")
    assert nodes == 332
    assert edges == 269
    assert labels == ["d", "a"]


def test_create_and_save_two_cycled_graph():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "graph.dot")
        create_and_save_two_cycled_graph(3, 4, ("x", "y"), file_path)
        assert os.path.exists(file_path)

        (pydot_graph,) = pydot.graph_from_dot_file(file_path)
        nodes = pydot_graph.get_nodes()
        edges = pydot_graph.get_edges()
        labels = {edge.get_attributes().get("label", "") for edge in edges}

        assert len(nodes) == 8
        assert len(edges) == 9
        assert labels == {"x", "y"}
