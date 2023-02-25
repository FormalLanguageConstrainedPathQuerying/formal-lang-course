import pytest
import os
import filecmp
from project import utils
import cfpq_data
import networkx
import random


def test_get_graph_info():

    tests = {
        "wc": {
            "number_of_nodes": 332,
            "number_of_edges": 269,
            "unique_labels": {"a", "d"},
        },
        "bzip": {
            "number_of_nodes": 632,
            "number_of_edges": 556,
            "unique_labels": {"a", "d"},
        },
        "pr": {
            "number_of_nodes": 815,
            "number_of_edges": 692,
            "unique_labels": {"a", "d"},
        },
        "ls": {
            "number_of_nodes": 1687,
            "number_of_edges": 1453,
            "unique_labels": {"a", "d"},
        },
        "gzip": {
            "number_of_nodes": 2687,
            "number_of_edges": 2293,
            "unique_labels": {"a", "d"},
        },
        "biomedical": {
            "number_of_nodes": 341,
            "number_of_edges": 459,
            "unique_labels": {
                "creator",
                "subClassOf",
                "title",
                "language",
                "versionInfo",
                "type",
                "publisher",
                "description",
                "label",
                "comment",
            },
        },
        "pathways": {
            "number_of_nodes": 6238,
            "number_of_edges": 12363,
            "unique_labels": {"subClassOf", "type", "label", "imports", "narrower"},
        },
    }

    for name in tests.keys():
        assert utils.get_graph_info(name) == tests[name]


def test_create_two_cycles_graph():
    path = "/tmp/two_cycles"

    for i in range(10):

        n = random.randint(1, 100)
        m = random.randint(1, 100)

        utils.create_two_cycles_graph((n, m), ("a", "b"), path)

        networkx.drawing.nx_pydot.write_dot(
            cfpq_data.labeled_two_cycles_graph(n, m, labels=("a", "b")),
            path + "_expect",
        )

        assert filecmp.cmp(path, path + "_expect")

        os.remove(path)
        os.remove(path + "_expect")
