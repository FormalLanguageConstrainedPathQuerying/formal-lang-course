import pytest
import cfpq_data as cd
from project import t4_ms_bfs_rpq as t4

DATASET_DIR = pathlib.Path(__file__).parent / "datasets"

@pytest.mark.parametrize(
    "filename, regex, start_nodes, final_nodes, exp_result",
    [
        ("regular_graph_1.csv", "abc", {0}, {0}, {(0, 0)}),
        ("regular_graph_1.csv", "abc", {0}, {2}, set()),
        ("regular_graph_1.csv", "a", {0}, {2}, set()),
        ("regular_graph_1.csv", "a", {0}, {1}, {(0, 1)}),
        ("regular_graph_2.csv", "*", {0, 1, 2}, {3}, {(0,3), (1,3), (2,3)}),
        ("regular_graph_2.csv", "xy", {0, 1, 2}, {3}, {(0,3)}),
        ("regular_graph_2.csv", "x(y|x)*", {0,3}, {3}, {(0,3), (3,3)}),
    ]
)
def simple_test(filename, regex, start_nodes, final_nodes, exp_result):
    filepath = str(DATASET_DIR / filename)
    graph = cd.graph_from_csv(filepath)
    result = t4.ms_bfs_based_rpq(regex, graph, start_nodes, final_nodes)
    assert result == exp_result
