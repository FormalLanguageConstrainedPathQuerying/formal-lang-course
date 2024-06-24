import random
from copy import deepcopy

import pytest
from to_program_parser import (
    WELL_TYPED,
    ILL_TYPED,
    GraphProgram,
    GrammarProgram,
    QueryProgram,
    to_program_parser,
)
from fixtures import graph
from grammars_constants import GRAMMARS_DIFFERENT
from networkx import MultiDiGraph
from pyformlang.cfg import CFG
from helper import generate_rnd_start_and_final, generate_rnd_dense_graph
from constants import LABELS

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
        graph_prog = GraphProgram(deepcopy(graph))
        cfg_prog = GrammarProgram(deepcopy(grammar))
        query = QueryProgram(
            graph_prog, cfg_prog, deepcopy(start_nodes), deepcopy(final_nodes)
        )
        program = query.full_program()
        assert typing_program(deepcopy(program))
        cfpq_from_prog = exec_program(deepcopy(program))[query.result_name]
        cfpq_from_algo = cfpq_with_matrix(
            deepcopy(grammar),
            deepcopy(graph),
            deepcopy(start_nodes),
            deepcopy(final_nodes),
        )
        assert cfpq_from_prog == cfpq_from_algo

    @pytest.mark.parametrize("queries_count", [1, 3, 5])
    def test_exec_many_graphs_many_queries(self, queries_count):
        query_list = []
        for i in range(queries_count):
            graph = generate_rnd_dense_graph(1, 40, LABELS)
            start_nodes, final_nodes = generate_rnd_start_and_final(deepcopy(graph))
            grammar_prog = GrammarProgram(random.choice(GRAMMARS_DIFFERENT))
            graph_prog = GraphProgram(deepcopy(graph))
            query_list.append(
                QueryProgram(
                    graph_prog,
                    grammar_prog,
                    deepcopy(start_nodes),
                    deepcopy(final_nodes),
                )
            )
        program, name_result = to_program_parser(query_list)
        assert typing_program(deepcopy(program))
        result_dict: dict = exec_program(deepcopy(program))
        for var, res in result_dict.items():
            query = name_result[var]
            query_full_program = query.full_program()
            assert typing_program(deepcopy(query_full_program))
            separate_res = exec_program(deepcopy(query_full_program))
            assert separate_res == res
            assert res == cfpq_with_matrix(
                query.get_grammar(),
                query.get_graph(),
                query.start_nodes,
                query.final_nodes,
            )
