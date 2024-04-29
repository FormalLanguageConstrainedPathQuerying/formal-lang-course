# This file contains test cases that you need to pass to get a grade
# You MUST NOT touch anything here except ONE block below
# You CAN modify this file IF AND ONLY IF you have found a bug and are willing to fix it
# Otherwise, please report it
import sys
from copy import deepcopy
import pytest

# Fix import statements in try block to run tests
try:
    from project.task11 import prog_to_tree, nodes_count, tree_to_prog
except ImportError:
    pytestmark = pytest.mark.skip("Task 11 is not ready to test!")

# it will be filled by script? In some way
INPUT_PROGRAMS = []


def fill_input(argv):
    for file_path in argv:
        with open(file_path, "r") as file:
            program = file.read()
            INPUT_PROGRAMS.append(program)


class TestParser:
    @pytest.mark.parametrize("program", INPUT_PROGRAMS, ids=lambda x: x)
    def id_test(self, program):
        tree_before = prog_to_tree(program)
        tree_after = prog_to_tree(tree_to_prog(tree_before))
        assert nodes_count(tree_before) == nodes_count(tree_after)
        assert program == tree_to_prog(tree_before)


if __name__ == "__main__":
    fill_input(sys.argv[1::])
