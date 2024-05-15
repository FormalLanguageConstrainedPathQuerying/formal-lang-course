import pytest
from to_program_parser import WELL_TYPED, ILL_TYPED, Program
from fixtures import graph
from grammars_constants import GRAMMARS_DIFFERENT
from networkx import MultiDiGraph
from pyformlang.cfg import CFG
from helper import generate_rnd_start_and_final

try:
    from project.task7 import cfpq_with_matrix
    from project.task12 import typing_program, exec_program
except ImportError:
    pytestmark = pytest.mark.skip("Task 12 is not ready to test!")


class TestTypeInference:
    @pytest.mark.parametrize("program", WELL_TYPED)
    def test_well_typed(self, program: str) -> None:
        assert typing_program(program)

    @pytest.mark.parametrize("program", ILL_TYPED)
    def test_ill_typed(self, program: str) -> None:
        assert not typing_program(program)

    @pytest.mark.parametrize("grammar", GRAMMARS_DIFFERENT)
    def test_exec_simple(self, graph: MultiDiGraph, grammar: CFG):
        start_nodes, final_nodes = generate_rnd_start_and_final(graph)
        program = Program(graph, grammar, start_nodes, final_nodes)
        assert typing_program(program)
        cfpq_from_prog = exec_program(str(program))[program.result_name]
        cfpq_from_algo = cfpq_with_matrix(grammar, graph, start_nodes, final_nodes)
        assert cfpq_from_prog == cfpq_from_algo
