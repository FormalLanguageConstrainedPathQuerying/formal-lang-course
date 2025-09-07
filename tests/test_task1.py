import pytest
from requests.exceptions import HTTPError

from project.task1 import (
    create_and_save_two_cycles_graph,
    get_graph_info,
)


def test_get_graph_info_bzip():
    info = get_graph_info("bzip")
    assert info["nodes"] == 632
    assert info["edges"] == 556
    assert info["labels"] == {"a", "d"}


def test_get_graph_info_nonexistent_graph():
    with pytest.raises(FileNotFoundError):
        get_graph_info("this_graph_does_not_exist")


def test_create_graph_two_cycles_graph(tmp_path):
    output_file = tmp_path / "test_graph.dot"
    nodes1, nodes2 = 4, 3
    labels = ("a", "b")

    create_and_save_two_cycles_graph(
        nodes_count1=nodes1,
        nodes_count2=nodes2,
        labels=labels,
        output_path=str(output_file),
    )

    assert output_file.exists()
    content = output_file.read_text()

    expected_content = """digraph {
1;
2;
3;
0;
4;
5;
1 -> 2 [key=0, label=a];
2 -> 3 [key=0, label=a];
3 -> 0 [key=0, label=a];
0 -> 1 [key=0, label=a];
0 -> 4 [key=0, label=b];
4 -> 5 [key=0, label=b];
5 -> 0 [key=0, label=b];
}
"""

    actual_content = output_file.read_text()

    assert actual_content == expected_content


def test_create_graph_one_node_cycle_self_loop_first(tmp_path):
    output_file = tmp_path / "test_graph.dot"
    create_and_save_two_cycles_graph(
        nodes_count1=1,
        nodes_count2=3,
        labels=("loop", "path"),
        output_path=str(output_file),
    )

    content = output_file.read_text()
    assert "0 -> 0 [key=0, label=loop];" in content
    assert "label=path" in content

def test_create_graph_one_node_cycle_self_loop_second(tmp_path):
    output_file = tmp_path / "test_graph.dot"
    create_and_save_two_cycles_graph(
        nodes_count1=3,
        nodes_count2=1,
        labels=("path", "loop"),
        output_path=str(output_file),
    )

    content = output_file.read_text()
    assert "0 -> 0 [key=0, label=loop];" in content
    assert "label=path" in content

def test_create_graph_one_node_cycle_self_loop_both(tmp_path):
    output_file = tmp_path / "test_graph.dot"
    create_and_save_two_cycles_graph(
        nodes_count1=1,
        nodes_count2=1,
        labels=("loop1", "loop2"),
        output_path=str(output_file),
    )

    content = output_file.read_text()
    assert "0 -> 0 [key=0, label=loop1];" in content
    assert "0 -> 0 [key=1, label=loop2];" in content

def test_create_graph_invalid_node_count():
    with pytest.raises(ValueError, match="node counts must be >= 1"):
        create_and_save_two_cycles_graph(0, 5, ("a", "b"), "dummy.dot")
    with pytest.raises(ValueError, match="node counts must be >= 1"):
        create_and_save_two_cycles_graph(5, -1, ("a", "b"), "dummy.dot")
