import pytest
from pyformlang.cfg import Terminal, Production

from project.cfg.io import *


class TestsReadFromFile:
    def test_read_cfg(self):
        str_path = "./resources/cfg1"
        path = Path(str_path)

        cfg = read_from_file(path)

        expected_terminals = ["a", "b"]
        expected_variables = ["S"]
        expected_start_symbol = "S"
        expected_productions = {
            Production(
                Variable("S"),
                [Terminal("a"), Variable("S"), Terminal("b"), Variable("S")],
            ),
            Production(Variable("S"), []),
        }

        assert cfg.start_symbol == expected_start_symbol
        assert cfg.terminals == set(
            map(lambda string: Terminal(string), expected_terminals)
        )
        assert cfg.variables == set(expected_variables)
        assert cfg.productions == expected_productions

    def test_file_not_found(self):
        not_exists_path = "./resources/not_exists"
        with pytest.raises(FileNotFoundError):
            read_from_file(Path(not_exists_path))
