from typing import Any, Iterable, Tuple
import networkx as nx
from networkx.utils.misc import graphs_equal
import pytest

from project.task1 import (
    GraphInfo,
    get_graph_info_via_name,
    save_labeled_two_cycles_graph,
)


@pytest.mark.parametrize(
    "graph_name,graph_info_expected",
    [("bzip", GraphInfo(node_count=632, edge_count=556, edge_labels=["d", "a"]))],
)
def test_get_graph_info_via_name(graph_name: str, graph_info_expected: GraphInfo):
    graph_info = get_graph_info_via_name(graph_name)
    assert graph_info == graph_info_expected


@pytest.mark.parametrize(
    "n,m,labels,path_to_expected_LTCG",
    [(5, 2, ("a", "b"), "tests/static/task1/5_2_ab.dot")],
)
def test_download_and_save_labeled_two_cycles_graph(
    n: int | Iterable[Any],
    m: int | Iterable[Any],
    labels: Tuple[str, str],
    path_to_expected_LTCG: str,
):
    PATH_TO_SAVE = "test_download_and_save_labeled_two_cycles_graph.dot"
    try:
        save_labeled_two_cycles_graph(
            n=n, m=m, labels=labels, path_to_save=PATH_TO_SAVE
        )
        LTCG = nx.nx_pydot.read_dot(PATH_TO_SAVE)
        LTCG_expected = nx.nx_pydot.read_dot(path_to_expected_LTCG)
        assert graphs_equal(LTCG, LTCG_expected)
    finally:
        from os import remove

        remove(PATH_TO_SAVE)
