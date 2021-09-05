import bridge

__all__ = ["run_console"]

_command_names = ("Quit", "GraphInfo", "CreateAndExport")
_function_pointers = {
    _command_names[0]: bridge.shutdown,
    _command_names[1]: bridge.graph_info,
    _command_names[2]: bridge.create_and_export,
}


def _exec_commands(commands: list) -> bool:
    is_command = False
    if commands[0] == _command_names[0]:
        _function_pointers[_command_names[0]](commands[1:])
        return False
    for comm_name in _command_names:
        if commands[0] == comm_name:
            is_command = True
            try:
                _function_pointers[comm_name](commands[1:])
            finally:
                print("End execute.")
    if not is_command:
        print("Invalid command")
    return True


def _help():
    print(
        "\n(1) GraphInfo [graph_name] : Get info about graph - number of nodes, number of edges, labels;"
    )
    print(
        "(2) CreateAndExport [filename] [nodes_number_first] [nodes_number_second] [label_1] [label_2]: create and "
        "export graph with two cycles;"
    )
    print("(3) Quit : Stop executable.")


def run_console():
    _help()
    continue_running = True
    while continue_running:
        stream = input(">>> ")
        commands = stream.split()
        continue_running = _exec_commands(commands)
