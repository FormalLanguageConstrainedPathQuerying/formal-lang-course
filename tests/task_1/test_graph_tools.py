import os
import pytest

from project.graph_tools import *

task_1_tests_dir_path = os.path.dirname(os.path.abspath(__file__))


def test_load_graph_with_bad_input():
    with pytest.raises(FileNotFoundError):
        load_graph("sebas")


# def test_load_graph_with_good_input():
#     g = load_graph("generations")
#     assert g.number_of_nodes() == 129
#     assert g.number_of_edges() == 273


def test_create_and_save_two_cycles_graph_0_0():
    with pytest.raises(IndexError):
        create_and_save_two_cycles_graph(0, 0, ["a1", "a2"], "both_cycles_is_empty.dot")


def test_create_and_save_two_cycles_graph_0_1():
    with pytest.raises(IndexError):
        create_and_save_two_cycles_graph(0, 1, ["a1", "a2"], "one_cycle_is_empty.dot")


def test_create_and_save_two_cycles_graph_1_0():
    with pytest.raises(IndexError):
        create_and_save_two_cycles_graph(1, 0, ["a1", "a2"], "one_cycle_is_empty.dot")


def test_create_and_save_two_cycles_graph_1_1():
    create_and_save_two_cycles_graph(1, 1, ["a1", "a2"], "test.dot")

    expected = open(
        os.sep.join([task_1_tests_dir_path, "expected/two_cycles_1_1_expected.dot"]),
        "r",
    ).read()

    assert open("test.dot", "r").read() == expected
    os.remove("test.dot")


def test_create_and_save_two_cycles_graph_1_2():
    create_and_save_two_cycles_graph(1, 2, ["bas", "sebas"], "test.dot")

    expected = open(
        os.sep.join([task_1_tests_dir_path, "expected/two_cycles_1_2_expected.dot"]),
        "r",
    ).read()

    assert open("test.dot", "r").read() == expected
    os.remove("test.dot")


# def test_get_graph_info_travel():
#     nodes_num, edges_num, labels = get_graph_info("travel")
#
#     assert nodes_num == 131
#     assert edges_num == 277
#
#     with open(
#         os.sep.join([task_1_tests_dir_path, "expected/travel_graph_labels.txt"])
#     ) as file:
#         expected_labels = [line.strip() for line in file]
#
#     assert labels == expected_labels
