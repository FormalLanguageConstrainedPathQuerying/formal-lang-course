import pytest
import project.graphs as proj
from tempfile import NamedTemporaryFile
from textwrap import dedent


def test_graph_info():
    # Самый маленький граф из датасета,
    # но метки на рёбрах всё равно очень большие
    info = proj.get_graph_info("skos")
    assert 144 == info.number_of_nodes
    assert 252 == info.number_of_edges


def test_graph_save():
    path = ""
    with NamedTemporaryFile(delete=False) as f:
        path = f.name
    proj.save_two_cycles(path, 2, 3, ("first", "second"))
    with open(path) as f:
        contents = "".join(f.readlines())
        expected = """\
            digraph  {
            1;
            2;
            0;
            3;
            4;
            5;
            1 -> 2  [key=0, label=first];
            2 -> 0  [key=0, label=first];
            0 -> 1  [key=0, label=first];
            0 -> 3  [key=0, label=second];
            3 -> 4  [key=0, label=second];
            4 -> 5  [key=0, label=second];
            5 -> 0  [key=0, label=second];
            }
            """
        expected = dedent(expected)
        contents = dedent(contents)
        assert expected == contents
