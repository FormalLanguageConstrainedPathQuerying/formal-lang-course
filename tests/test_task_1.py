import filecmp
import os
from pathlib import Path

import pytest

from project.graph_lib import get_graph_info, GraphInformation, generate_and_write_two_cycles_graph


def test_get_graph_info():
    actual_info = get_graph_info("people")

    expected_info = GraphInformation(
        337,
        640,
        {
            "allValuesFrom",
            "comment",
            "complementOf",
            "disjointWith",
            "domain",
            "drives",
            "equivalentClass",
            "first",
            "has_pet",
            "intersectionOf",
            "inverseOf",
            "is_pet_of",
            "label",
            "maxCardinality",
            "minCardinality",
            "onProperty",
            "range",
            "reads",
            "rest",
            "service_number",
            "someValuesFrom",
            "subClassOf",
            "subPropertyOf",
            "type",
            "unionOf",
        },
    )
    assert actual_info == expected_info


def test_no_name_graph():
    with pytest.raises(Exception):
        get_graph_info("this_name_surely_does_not_exist")


def test_generate_two_cycles_graph():
    gen_path = Path(Path(__file__).parent, "files", "generated.dot")
    expect_path = Path(Path(__file__).parent, "files", "expected.dot")

    generate_and_write_two_cycles_graph(3, 2, ("x", "y"), gen_path)

    assert filecmp.cmp(expect_path, gen_path)
    os.remove(gen_path)


def test_generate_graph_without_cycles():
    gen_path = Path(Path(__file__).parent, "files", "non_exist.dot")
    with pytest.raises(Exception):
        generate_and_write_two_cycles_graph(
            0, 0, ("x", "y"), gen_path
        )
