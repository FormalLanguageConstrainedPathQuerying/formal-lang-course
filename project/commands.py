import os
import sys
from pathlib import Path

import networkx
import pydot

from graphs import generate_and_save_two_cycles, get_graph_info


class ExecutionException(Exception):
    """Exception raised for errors in the execution.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


def graph_info(graph_filename: str):
    file = Path(graph_filename)
    _, extension = os.path.splitext(graph_filename)
    if not file.is_file():
        raise ExecutionException("No such file exists!")
    if extension != ".dot":
        raise ExecutionException("Wrong extension of file!")
    pydot_graph = pydot.graph_from_dot_file(graph_filename)[0]
    graph = networkx.drawing.nx_pydot.from_pydot(pydot_graph)
    info = get_graph_info(graph)
    print("Information about graph")
    print(info)


def create_and_save(
    filename, nodes_first_num, nodes_second_num, label_first, label_second
):
    file = Path(filename)
    if not file.is_file():
        open(filename, "w")
    generate_and_save_two_cycles(
        int(nodes_first_num),
        int(nodes_second_num),
        (label_first, label_second),
        filename,
    )
    print("Graph has been created and saved.")


def quit_app():
    print("Quit...")
    sys.exit(0)
