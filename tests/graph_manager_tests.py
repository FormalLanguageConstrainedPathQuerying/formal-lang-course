from project.graph_manager import *

import pytest


def get_graph_info_test():
    G = get_graf_information_by_name("skos")
    assert G[0] == 144
    assert G[1] == 252
    assert len(G[2]) == 21


def create_and_write_graph_test():
    create_graph_by_number_vertices_in_loops_and_label_names_and_save_in_file(
        5, 3, ("fst", "snd"), "testCreateGraph.dot"
    )
    with open("testCreateGraph.dot", "r") as f:
        assert (
            "digraph  { 1; 2; 3; 4; 5; 0; 6; 7; 8; 1 -> 2  [key=0, label=fst]; 2 -> 3  [key=0, label=fst]; 3 -> 4  "
            "[key=0, label=fst]; 4 -> 5  [key=0, label=fst]; 5 -> 0  [key=0, label=fst]; 0 -> 1  [key=0, "
            "label=fst]; 0 -> 6  [key=0, label=snd]; 6 -> 7  [key=0, label=snd]; 7 -> 8  [key=0, label=snd]; 8 -> "
            "0  [key=0, label=snd]; } " == f.read().replace("\n", " ")
        )
