import project.graph as graph
import cfpq_data.dataset.data as ds
import pytest
import pydot


class TestCrAndSave2CycGraph:
    def test_read_after_write(self):
        graph.create_and_safe_2cycle_graph(10, 10, ("a", "b"), "ex.dot")
        g = pydot.graph_from_dot_file("ex.dot")[0]
        assert len(g.get_node_list()) == 21
        assert len(g.get_edge_list()) == 22
        assert {edge.obj_dict["attributes"]["label"] for edge in g.get_edge_list()} == {
            "a",
            "b",
        }


class TestGraphInfo:
    def test_nonneg_graph_info(self):
        infos = map(lambda name: graph.Info.from_file(name), ds.DATASET[0:3])
        for info in infos:
            assert info.number_of_nodes() >= 0
            assert info.number_of_edges() >= 0

    def test_nonexisting_graph_info(self):
        with pytest.raises(FileNotFoundError):
            graph.Info.from_file("")
