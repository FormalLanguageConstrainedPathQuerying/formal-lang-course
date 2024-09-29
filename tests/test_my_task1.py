import os
import pytest
from project import task1


class TestGraphUtils:
    def test_info_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            task1.get_info_from_graph_name("no_such_file")

    def test_info_bzip(self):
        info = task1.get_info_from_graph_name("bzip")
        # https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/graphs/data/bzip.html#bzip
        bzip = (632, 556, ["d", "a"])
        assert info == bzip

    def test_write_file_exists(self):
        file_name = "52.dot"
        graph_info = (52, 52, ("5", "2"))
        task1.create_two_cycles_graph_and_write_to_dot(*graph_info, file_name)
        assert os.path.isfile(file_name)
        os.remove(file_name)

    def test_write_file_is_correct(self):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        graph_path = "52.dot"
        graph_info = (52, 52, ("5", "2"))
        task1.create_two_cycles_graph_and_write_to_dot(*graph_info, graph_path)
        assert (
            open(graph_path, "r").read()
            == open(
                os.path.join(root_dir, "test_graphs/test_write_file_is_correct.dot"),
                "r",
            ).read()
        )
        os.remove(graph_path)
