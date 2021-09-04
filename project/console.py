import project
from project.commands import ExecutionException

command_names = ["graph_info", "create_and_save", "quit"]

command_dict = {
    command_names[0]: project.commands.graph_info,
    command_names[1]: project.commands.create_and_save,
    command_names[2]: project.commands.quit_app,
}


class InputException(Exception):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


def print_options():
    print(
        "\n(1) graph_info [graph_name] : Get info about graph - number of nodes, number of edges, labels;"
    )
    print(
        "(2) create_and_save [filename] [nodes_number_first] [nodes_number_second] [label_1] [label_2]: create and "
        "save graph with two cycles;"
    )
    print("(3) quit : Quit application.")


def check_command(input_split):
    current_command_name = input_split[0]
    if current_command_name not in command_names:
        raise InputException("Command not found!")
    if current_command_name == command_names[0]:
        if len(input_split) != 2:
            raise InputException("Error in argument's number!")
    elif current_command_name == command_names[1]:
        if len(input_split) != 6:
            raise InputException("Error in argument's number!")
        if not input_split[2].isnumeric() or not input_split[3].isnumeric():
            raise InputException("Wrong types of arguments!")
    elif current_command_name == command_names[2]:
        if len(input_split) != 1:
            raise InputException("Error in argument's number!")


def run():
    print_options()
    while True:
        input_text = input(">>> ")
        input_split = input_text.split(sep=" ")
        try:
            check_command(input_split)
        except InputException as ie:
            print(ie.message + " Try again!")
            continue
        name = input_split[0]
        try:
            command_dict[name](*input_split[1:])
        except ExecutionException as ee:
            print(ee.message + " Try again!")
            continue
