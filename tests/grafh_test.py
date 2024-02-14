import pytest
import os
from project.task_1 import get_graph_info, build_and_save_graph

def test_get_graph_info():
    num_vertices, num_edges, edge_labels = get_graph_info("example_graph")
    assert num_vertices == 3
    assert num_edges == 3
    assert set(edge_labels) == {'A', 'B', 'C'}

def test_build_and_save_graph(tmp_path):
    output_file = os.path.join(tmp_path, "output_graph.dot")
    build_and_save_graph(3, ['A', 'B', 'C'], output_file)
    assert os.path.exists(output_file)
    with open(output_file, 'r') as f:
        content = f.read()
        assert 'graph {' in content
        assert '0 -- 1 [label="A"]' in content
        assert '1 -- 2 [label="B"]' in content
        assert '2 -- 0 [label="C"]' in content

