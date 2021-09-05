from pathlib import Path
import networkx
import pydot
import utils

__all__ = ["graph_info", "create_and_export", "shutdown"]


def _is_file(filename):
    """
    Checks if the passed value is a file.
    :param filename:
    :return:
    """
    file = Path(filename)
    return file.is_file()


def _read_graph(filename: str):
    """
    Reading the graph.
    :param filename:
    :return:
    """
    pydot_graph = pydot.graph_from_dot_file(filename)[0]
    return networkx.drawing.nx_pydot.from_pydot(pydot_graph)


def graph_info(arg: list):
    """
    Reading graph by name and display information about it.
    :param arg:
    :return:
    """
    if len(arg) != 1:
        raise Exception("Invalid amount of arguments!")
    filename = arg[0]
    name, extension = filename.split(".")
    if not _is_file(filename):
        raise Exception("No such file exists!")
    if extension != "dot":
        raise Exception("Wrong extension of file!")
    graph = _read_graph(filename)
    info = utils.get_graph_info(graph)
    print("Graph information:")
    print("Number of nodes: ", info[0])
    print("Number of edges: ", info[1])
    print("Labels: ", *(info[2]))


def create_and_export(arg: list):
    """
    Call method for generate and export graph.
    :param arg:
    :return:
    """
    if len(arg) != 5:
        raise Exception("Invalid amount of arguments!")
    if not _is_file(arg[0]):
        open(arg[0], "w")
    utils.generate_and_export_two_cycle(
        int(arg[1]),
        int(arg[2]),
        (arg[3], arg[4]),
        arg[0],
    )
    print("Graph has been created and saved.")


def shutdown(arg: list):
    print("Finishing work.")
