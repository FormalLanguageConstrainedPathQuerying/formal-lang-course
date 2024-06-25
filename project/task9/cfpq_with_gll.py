from collections import deque

import networkx as nx
from pyformlang.cfg import CFG
from pyformlang.finite_automaton import State
from pyformlang.rsa import RecursiveAutomaton

from project.task8.cfpq_with_tensors import cfg_to_rsm


def cfpq_with_gll(
    rsm: RecursiveAutomaton,
    graph: nx.DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
) -> set[tuple[int, int]]:
    """
    Выполняет контекстно-свободный запрос пути (CFPQ) с использованием алгоритма GLL.

    :param rsm: Рекурсивный автомат (RSM).
    :param graph: Направленный граф (DiGraph).
    :param start_nodes: Набор начальных узлов.
    :param final_nodes: Набор конечных узлов.
    :return: Набор пар достижимых состояний (начальный узел, конечный узел).
    """
    if isinstance(rsm, CFG):
        rsm = cfg_to_rsm(rsm)

    start_nodes = start_nodes or set(graph.nodes)
    final_nodes = final_nodes or set(graph.nodes)

    start_nonterminal = (
        rsm.initial_label.value if rsm.initial_label.value is not None else "S"
    )
    start_state = rsm.boxes[rsm.initial_label].dfa.start_state.value

    return _perform_gll(
        rsm, graph, start_nonterminal, start_state, start_nodes, final_nodes
    )


def _perform_gll(rsm, graph, start_nonterminal, start_state, start_nodes, final_nodes):
    """
    Основная функция для выполнения обхода графа и поиска путей с использованием алгоритма GLL.

    :param rsm: Рекурсивный автомат (RSM).
    :param graph: Направленный граф (DiGraph).
    :param start_nonterminal: Начальный нетерминал.
    :param start_state: Начальное состояние RSM.
    :param start_nodes: Набор начальных узлов.
    :param final_nodes: Набор конечных узлов.
    :return: Набор пар достижимых состояний (начальный узел, конечный узел).
    """
    result = set()
    visited = set()
    queue = deque()

    for start_node in start_nodes:
        queue.append((start_nonterminal, start_node, start_node))

    dfa_dict = rsm.boxes[start_nonterminal].dfa.to_dict()
    dfa_dict.setdefault(State(start_state), dict())

    while queue:
        current_nonterminal, current_node, path_start = queue.popleft()

        if (current_node, (path_start, current_nonterminal)) in visited:
            continue

        visited.add((current_node, (path_start, current_nonterminal)))

        if _is_final_state(current_node, final_nodes, current_nonterminal, start_state):
            result.add((path_start, current_node))

        _process_dfa_transitions(
            dfa_dict, rsm, current_nonterminal, current_node, path_start, visited, queue
        )
        _process_graph_neighbors(
            graph, current_nonterminal, current_node, path_start, visited, queue
        )

    return result


def _is_final_state(current_node, final_nodes, current_nonterminal, start_state):
    """
    Проверяет, является ли текущее состояние конечным состоянием.
    """
    return current_node in final_nodes and current_nonterminal == start_state


def _process_dfa_transitions(
    dfa_dict, rsm, current_nonterminal, current_node, path_start, visited, queue
):
    """
    Обрабатывает переходы по символам DFA.
    """
    for symbol, _ in dfa_dict.items():
        if symbol in rsm.labels:
            new_state = (current_nonterminal, current_node, symbol.value)
            if new_state not in visited:
                queue.append((symbol.value, current_node, path_start))


def _process_graph_neighbors(
    graph, current_nonterminal, current_node, path_start, visited, queue
):
    """
    Обрабатывает соседние узлы текущего узла графа.
    """
    for neighbor in graph.neighbors(current_node):
        if (current_nonterminal, neighbor, path_start) not in visited:
            queue.append((current_nonterminal, neighbor, path_start))
