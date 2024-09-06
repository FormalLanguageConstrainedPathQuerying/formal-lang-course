import os
from pathlib import Path

import pytest

from project.graph_module import Graph


class TestGraph:
    def test_name_graph(self):
        with pytest.raises(FileNotFoundError):
            Graph.load_graph("Lesh79")

    def test_graph_info_bzip(self):
        graph_info_bzip = (632, 556, ["d", "a"])
        assert Graph.graph_info("bzip") == graph_info_bzip

    def test_graph_info_pizza(self):
        graph_info_pizza = (
            671,
            1980,
            [
                "disjointWith",
                "type",
                "subClassOf",
                "onProperty",
                "first",
                "rest",
                "someValuesFrom",
                "label",
                "allValuesFrom",
                "comment",
                "unionOf",
                "equivalentClass",
                "intersectionOf",
                "range",
                "domain",
                "hasValue",
                "distinctMembers",
                "subPropertyOf",
                "complementOf",
                "inverseOf",
                "versionInfo",
                "minCardinality",
                "oneOf",
            ],
        )
        assert Graph.graph_info("pizza") == graph_info_pizza

    def test_create_labeled_graph(self):
        path_to_file: str = "test_create.dot"
        Graph.create_labeled_graph(5, 12, ("11", "12"), path_to_file)
        assert (
                open(path_to_file, "r").read()
                == open(Path("tests/test_create_graph_expected.dot"), "r").read()
        )
        os.remove(path_to_file)
