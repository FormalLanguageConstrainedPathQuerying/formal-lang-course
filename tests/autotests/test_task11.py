# This file contains test cases that you need to pass to get a grade
# You MUST NOT touch anything here except ONE block below
# You CAN modify this file IF AND ONLY IF you have found a bug and are willing to fix it
# Otherwise, please report it
import sys
from copy import deepcopy
import pytest
import re

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
    def id_test(self, program: str):
        tree_before, is_valid = prog_to_tree(program)
        assert is_valid
        program_after = tree_to_prog(tree_before)
        tree_after, _ = prog_to_tree(program_after)
        assert nodes_count(tree_before) == nodes_count(tree_after)
        assert program == program_after
        reg = re.compile("[=,]", re.X)
        if reg.search(program):
            program_bad = reg.sub("", program)
            _, is_valid_bad = prog_to_tree(program_bad)
            assert not is_valid_bad
