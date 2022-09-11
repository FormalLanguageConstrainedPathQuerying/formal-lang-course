import project.graph_module as gm


def test_get_graph_count_vertex_edges_labels():
    expected_result = (332, 269, {"D", "A"})
    actual_result = gm.get_graph_count_vertex_edges_labels("wc")
    assert expected_result == actual_result


def test_build_two_cycles_graph_dot_format(tmp_path):
    actual_file_path = tmp_path / "actual_test_graph.dot"
    gm.build_two_cycles_graph_dot_format(1, 2, ("man", "woman"), actual_file_path)
    assert (
        open(actual_file_path, "r").read()
        == """digraph  {
1;
0;
2;
3;
1 -> 0  [key=0, label=man];
0 -> 1  [key=0, label=man];
0 -> 2  [key=0, label=woman];
2 -> 3  [key=0, label=woman];
3 -> 0  [key=0, label=woman];
}
"""
    )
