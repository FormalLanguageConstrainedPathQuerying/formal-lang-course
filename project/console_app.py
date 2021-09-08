from typing import List

from project.console_commands import *

__all__ = ["repl"]

command_names = (
    "exit",
    "get_description",
    "get_two_cycles",
    "save_to_dot",
    "get_names",
)

command_names_commands = {
    command_names[0]: exit_repl,
    command_names[1]: get_graph_description,
    command_names[2]: get_two_cycles_graph,
    command_names[3]: save_graph_to_dot,
    command_names[4]: get_graph_names,
}

description = f"""
Supported commands:
- {command_names[0]}
- {command_names[1]} [name: str]
- {command_names[2]} [first_cycle: int] [second_cycle: int] [first_label: str] [second_label: str]
- {command_names[3]} [path: str] [name: str]
- {command_names[4]}
"""


def analyse_input(inputs: List[str]) -> None:
    """
    Analyze whether list of input strings matches to application commands.

    Parameters
    ----------
    inputs: List[str]
       List of input strings

    Returns
    -------
    None

    Raises
    ------
    SyntaxError
        If number of command parameters was wrong
    TypeError
        If command parameter has wrong type
    """

    command_name = inputs[0]

    if command_name not in command_names:
        raise SyntaxError(
            f'Command "{command_name}" is not supported: use commands from the list'
        )

    if (
        command_name == command_names[0] or command_name == command_names[4]
    ) and not len(inputs) == 1:
        raise SyntaxError("Wrong arguments count, it must be empty")

    if command_name == command_names[1] and not len(inputs) == 2:
        raise SyntaxError("Wrong arguments count, it must be one")

    if command_name == command_names[2]:
        if not len(inputs) == 5:
            raise SyntaxError("Wrong arguments count, it must be four")

        if not inputs[1].isnumeric() or not inputs[2].isnumeric():
            raise TypeError(
                "Wrong type of count of nodes in cycles, it must be a number"
            )

        for i in (inputs[3], inputs[4]):
            if not i.isalpha():
                raise TypeError(
                    "Wrong type of edge labels, it must be a chars (strings)"
                )

    if command_name == command_names[3] and not len(inputs) == 3:
        raise SyntaxError("Wrong arguments count, it must be two")


def repl() -> None:
    """
    Runs a console application.

    Returns
    -------
    None
    """

    print(f"\n{description}\n")

    while True:
        inputs = input(">>> ").strip().split(" ")
        # remove ""
        inputs = list(filter(None, inputs))
        # get pure commands
        for _ in inputs:
            i = inputs.pop(0)
            i = i.strip()
            inputs.append(i)

        try:
            analyse_input(inputs)
        except (SyntaxError, TypeError) as errs:
            print(f"\n{errs}\n")
            continue

        command_name = inputs[0]
        arguments = inputs[1:]

        try:
            command_names_commands[command_name](*arguments)
        except (SyntaxError, NameError, IndexError) as errs:
            print(f"\n{errs}\n")
            continue
