from project.utils import graph_utils
from project.utils.graph_utils import GraphException
from typing import Callable
from functools import wraps

import sys

__all__ = ["GraphShell", "ExecutionException"]


class ExecutionException(Exception):
    """
    Base exception for GraphShell REPL

    Attributes
    ----------
    msg : str
        Error message
    """

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg


class Environment:
    """
    Data storage, stores useful data for REPL.

    Attributes
    ----------
    graphs : dict
        Graphs storage
    """

    def __init__(self):
        self.graphs = {}


class GraphShell:
    """
    Class represents REPL

    Attributes
    ----------
    greet_msg : str
        Message printed when repl starts
    end_msg : str
        Message printed when repl ends
    prompt : str
        Message printed every loop, before reading command
    commands : tuple
        Available commands
    env : Environment
        REPL environment
    """

    class Decorators:
        """
        Decorator class for error handling
        """

        @classmethod
        def eval_command(cls, cmd: Callable):
            @wraps(cmd)
            def call_command(*args, **kwargs):
                try:
                    cmd(*args, **kwargs)
                except ExecutionException as e:
                    print(e)
                except GraphException as e:
                    print(e)

            return call_command

    def __init__(self):
        self.greet_msg = "=== GraphShell REPL. Type help to list possible commands. ==="
        self.end_msg = "=== Shutting down ==="
        self.prompt = ">>> "
        self.commands = (
            "get_graph_info",
            "generate_two_cycles_graph",
            "save_to_dot",
            "quit",
            "help",
        )
        self.env = Environment()

    @Decorators.eval_command
    def do_get_graph_info(self, *args):
        """get_graph_info < name > -- Returns info about the given graph"""
        if len(args) != 1:
            raise ExecutionException(
                f"get_graph_info takes 1 positional arguments, but {len(args)} were given"
            )

        print(graph_utils.get_graph_info(name=args[0], env=self.env.graphs))

    @Decorators.eval_command
    def do_generate_two_cycles_graph(self, *args):
        """generate_two_cycles_graph <name> <first_cycle_nodes_num>  <second_cycle_nodes_num>  <first_cycle_label>
        <second_cycle_label> -- Generates two cycles graph with given name, save it to environment table of graphs"""
        if len(args) != 5:
            raise ExecutionException(
                (
                    f"generate_two_cycles_graph takes 5 positional arguments, "
                    f"but {len(args)} was given"
                )
            )

        graph = graph_utils.generate_two_cycles_graph(*args[1:])
        self.env.graphs.update({args[0]: graph})

        print(f"Successfully created graph '{args[0]}'")

    @Decorators.eval_command
    def do_save_to_dot(self, *args):
        """save_to_dot <name> <path_to_file>"""
        if len(args) != 2:
            raise ExecutionException(f"save_to_dot takes 2 positional arguments")

        graph = graph_utils.get_graph(args[0], self.env.graphs)

        path = graph_utils.save_to_dot(graph, args[1])
        print(f"Successfully saved graph '{args[0]}' to '{path}'")

    @Decorators.eval_command
    def do_quit(self, *args):
        """quit -- Quit from REPL"""

        if len(args) != 0:
            raise ExecutionException(
                f"quit takes 0 positional arguments, but {len(args)} were given"
            )

        print(self.end_msg)
        sys.exit(0)

    @Decorators.eval_command
    def do_help(self, *args):
        """help [command] -- list all methods or get information about specific 'command'"""

        if len(args) > 1:
            raise ExecutionException(
                f"help takes 0 or 1 positional arguments, but {len(args)} were given"
            )

        if len(args) == 0:
            print(f"Commands: {self.commands}")
        else:
            print(self.get_command(args[0]).__doc__)

    def get_command(self, name):
        """
        Get command function from commands

        Parameters
        ----------
        name : str
            Name of command

        Returns
        -------
        cmd : Callable
            Command function object

        Raises
        ------
        ExecutionException
            If name is absent in commands
        """
        if name in self.commands:
            return getattr(self, "do_" + name)
        raise ExecutionException(
            f"Unknown command '{name}'. Print 'help' to list all commands."
        )

    def loop(self):
        """
        Evaluation loop
        """
        print(self.greet_msg)
        while True:
            raw_input = input(self.prompt)
            func_name, args = self.parse(raw_input)
            try:
                self.get_command(func_name)(*args)
            except ExecutionException as e:
                print(e)

    @staticmethod
    def parse(raw_input: str):
        """
        Parses given raw input into tokens

        Parameters
        ----------
        raw_input : str
            Raw input

        Returns
        -------
        tokens : Tuple[str, str]
            Tuple, where first element is function name, and second is argument list
        """
        tokens = raw_input.split()
        return tokens[0], tokens[1:]
