import networkx as nx
import pyformlang
from pyformlang.cfg import Epsilon
from pyformlang.finite_automaton import Symbol
from pyformlang.regular_expression import Regex
from pyformlang.rsa import Box, RecursiveAutomaton
from pyformlang.cfg import CFG
from scipy.sparse import dok_matrix, eye
from project.task2 import graph_to_nfa
from project.task3 import (
    FiniteAutomaton,
    transitive_closure,
    intersect_automata,
    rsm_to_fa,
)


def cfpq_with_tensor(
    rsm: RecursiveAutomaton,
    graph: nx.MultiDiGraph,
    final_nodes: set[int] = None,
    start_nodes: set[int] = None,
) -> set[tuple[int, int]]:
    rsm_fa = rsm_to_fa(rsm)
    graph_finite_automaton = FiniteAutomaton(
        graph_to_nfa(graph, start_nodes, final_nodes)
    )
    matrix_indexes = rsm_fa.revert_mapping()
    graph_indexes = graph_finite_automaton.revert_mapping()

    _size = len(graph_finite_automaton.states_mapping)
    for eps in rsm_fa.eps:
        if eps not in graph_finite_automaton.matrix:
            graph_finite_automaton.matrix[eps] = dok_matrix((_size, _size), dtype=bool)
        graph_finite_automaton.matrix[eps] += eye(_size, dtype=bool)

    closure = transitive_closure(intersect_automata(rsm_fa, graph_finite_automaton))
    closure = list(zip(*closure.nonzero()))

    for _start, _final in closure:
        frm = matrix_indexes[_start // _size]
        to = matrix_indexes[_final // _size]

        if frm in rsm_fa.start_states and to in rsm_fa.final_states:
            _symbol = frm.value[0]
            if _symbol not in graph_finite_automaton.matrix:
                graph_finite_automaton.matrix[_symbol] = dok_matrix(
                    (_size, _size), dtype=bool
                )
            graph_finite_automaton.matrix[_symbol][
                _start % _size, _final % _size
            ] = True

    result = set()
    for matrix in graph_finite_automaton.matrix.values():
        for _start, _final in zip(*matrix.nonzero()):
            if (
                graph_indexes[_start] in rsm_fa.start_states
                and graph_indexes[_final] in rsm_fa.final_states
            ):
                result.add((graph_indexes[_start], graph_indexes[_final]))

    return result


def cfg_to_rsm(cfg: CFG) -> RecursiveAutomaton:
    productions = {}
    boxes = set()
    labels = set()
    for production in cfg.productions:
        if len(production.body) == 0:
            regex = Regex(
                " ".join(
                    "$" if isinstance(var, Epsilon) else var.value
                    for var in production.body
                )
            )
        else:
            regex = Regex("$")
        head = Symbol(production.head)
        labels.add(head)
        if head not in productions:
            productions[head] = regex
        else:
            productions[head] = productions[head].union(regex)

    for head, body in productions.items():
        boxes.add(Box(body.to_epsilon_nfa().minimize(), head))

    return pyformlang.rsa.RecursiveAutomaton(labels, Symbol("S"), boxes)


def ebnf_to_rsm(ebnf: str) -> pyformlang.rsa.RecursiveAutomaton:
    return pyformlang.rsa.RecursiveAutomaton.from_text(ebnf)


if __name__ == "__main__":
    pass
