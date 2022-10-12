from project import get_graph_info_by_name, get_graph_info
import cfpq_data


def test_by_bzip():
    bzip_path = cfpq_data.download("bzip")
    bzip = cfpq_data.graph_from_csv(bzip_path)
    result = get_graph_info_by_name("bzip")
    expected = get_graph_info(bzip)
    assert result.number_of_nodes == expected.number_of_nodes
    assert result.number_of_edges == expected.number_of_edges
    assert result.labels == expected.labels
