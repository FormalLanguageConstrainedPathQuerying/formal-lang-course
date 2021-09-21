import os
import sys
from pathlib import Path

from project.graph_tools import *

__all__ = [
    "exit_repl",
    "get_graph_description",
    "get_two_cycles_graph",
    "save_graph_to_dot",
    "get_graph_names",
]


def exit_repl() -> None:
    """
    Implementation of application exit command.

    Exits the REPL.

    Returns
    -------
    None
    """

    sys.exit(0)


def get_graph_description(name: str) -> None:
    """
    Implementation of get_graph_description application command.

    Prints description of graph by it's real dataset name.

    Parameters
    ----------
    name: str
        Real dataset graph name from https://jetbrains-research.github.io/CFPQ_Data/dataset/index.html.

    Returns
    -------
    None
    """

    description = get_description(name)

    print(
        f"""
        Description of graph "{description.name}":
        {str(description)}
        """
    )


def get_two_cycles_graph(
    first_cycle: int, second_cycle: int, *edge_labels: str
) -> None:
    """
    Implementation of generate_two_cycles_graph application command.

    Generates two cycles graph specified by parameters and prints it's description.

    Parameters
    ----------
    first_cycle: int
        Number of nodes in the first cycle without common node
    second_cycle: int
        Number of nodes in the second cycle without common node
    edge_labels: Tuple[str, ...]
        Edge labels on the cycles

    Returns
    -------
    None
    """

    description = get_two_cycles(
        first_cycle, second_cycle, (edge_labels[0], edge_labels[1])
    ).description

    print(
        f"""
        Two cycles graph "{description.name}" with
        {str(description)}
        was successfully generated
        """
    )


def save_graph_to_dot(path: str, name: str) -> None:
    """
    Implementation of save_current_graph_to_dot application command.

    Saves graph by name to "*.dot" file specified by path and prints it's description.

    Parameters
    ----------
    path: str
        Path to save the graph, extension ".dot" required
    name: str
        Name of graph to save from ever used graphs

    Returns
    -------
    None

    Raises
    ------
    SyntaxError
        If extension wasn't ".dot"
    """

    _, ext = os.path.splitext(path)

    if not ext == ".dot":
        raise SyntaxError('Wrong extension, ".dot" is required')

    file = Path(path)

    if not file.exists() or not file.is_file():
        open(path, "w+")

    description = save_to_dot(path, name)

    print(
        f"""
        Graph "{description.name}" with
        {str(description)}
        was successfully saved in
        {str(file)}
        """
    )


def get_graph_names() -> None:
    """
    Gets names list of ever used graphs and prints it

    Returns
    -------
    None
    """

    names = get_names()

    print("\n\tGraph names have ever been used:")
    if len(names) == 0:
        print("\tempty")
    else:
        for n in names:
            print(f"\t- {n}")
    print()
