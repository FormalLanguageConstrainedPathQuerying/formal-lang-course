import os
from project.graph_utils import GraphUtils


def test_get_graph_info():
    graph_info = GraphUtils.get_graph_info("atom")
    # Based on https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/graphs/data/atom.html#atom
    assert graph_info.number_of_nodes == 291
    assert graph_info.number_of_edges == 425
    assert len(graph_info.labels_set) == 17


def test_save_labeled_two_cycles_graph():
    GraphUtils.save_labeled_two_cycles_graph(
        [0, 2, 4, 6], [1, 3, 5, 6], 6, "tests/test_files/output_raw.dot"
    )
    assert os.path.exists("tests/test_files/output_raw.dot")
    os.remove("tests/test_files/output_raw.dot")
