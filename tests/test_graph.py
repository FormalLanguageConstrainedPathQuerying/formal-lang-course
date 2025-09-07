import project.graph as graph
import cfpq_data
import cfpq_data.dataset.data as ds
import pytest
import networkx
import pydot


class TestCrAndSave2CycGraph:
    def test_read_after_write(self):
        graph.create_and_safe_2cycle_graph(10, 10, ("a", "b"), "ex.dot")
        g = networkx.drawing.nx_pydot.from_pydot(pydot.graph_from_dot_file("ex.dot"))
        assert g.number_of_nodes == 21
        assert g.number_of_edges == 22
        assert {edge.label for edge in g.edges} == {"a", "b"}


class TestGraphInfo:
    def test_nonneg_graph_info(self):
        infos = (ds.DATASET[0:3]).map(graph.Info)
        for info in infos:
            assert info.number_of_nodes >= 0
            assert info.number_of_edges >= 0

    def test_nonexisting_graph_info(self):
        with pytest.raises(FileNotFoundError):
            graph.Info("")
