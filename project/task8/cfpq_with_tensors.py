import networkx as nx
from pyformlang.cfg import CFG
from pyformlang.rsa import RecursiveAutomaton
from itertools import product
from scipy.sparse import dok_matrix, eye, kron

from project.task3.finite_automaton import FiniteAutomaton, rsm_to_fa
from project.task2.fa_builders import graph_to_nfa


def cfg_to_rsm(cfg: CFG) -> RecursiveAutomaton:
    """
    Преобразует контекстно-свободную грамматику (CFG) в рекурсивный автомат (RSM).

    :param cfg: Контекстно-свободная грамматика (CFG).
    :return: Рекурсивный автомат (RSM).
    """
    return RecursiveAutomaton.from_text(cfg.to_text())


def ebnf_to_rsm(ebnf: str) -> RecursiveAutomaton:
    """
    Преобразует грамматику в расширенной форме Бэкуса-Наура (EBNF) в рекурсивный автомат (RSM).

    :param ebnf: Грамматика в расширенной форме Бэкуса-Наура (EBNF).
    :return: Рекурсивный автомат (RSM).
    """
    return RecursiveAutomaton.from_text(ebnf)


def cfpq_with_tensor(
    rsm: RecursiveAutomaton,
    graph: nx.MultiDiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
) -> set[tuple[int, int]]:
    """
    Выполняет контекстно-свободный запрос пути (CFPQ) с использованием метода тензорного произведения.

    :param rsm: Рекурсивный автомат (RSM).
    :param graph: Направленный мультиграф (MultiDiGraph).
    :param start_nodes: Набор начальных узлов.
    :param final_nodes: Набор конечных узлов.
    :return: Набор пар достижимых состояний (начальный узел, конечный узел).
    """
    if isinstance(rsm, CFG):
        rsm = cfg_to_rsm(rsm)

    start_nodes = start_nodes or set(graph.nodes)
    final_nodes = final_nodes or set(graph.nodes)

    fa_rsm = rsm_to_fa(rsm)
    fa_graph = FiniteAutomaton(graph_to_nfa(graph, start_nodes, final_nodes))

    state_mapping = initialize_state_mapping(fa_graph, fa_rsm)
    num_rsm_states, num_graph_states = len(fa_rsm.states), len(fa_graph.states)
    num_states = num_rsm_states * num_graph_states

    previous_non_zeros = 0
    while True:
        common_symbols = fa_rsm.matrix.keys() & fa_graph.matrix.keys()
        if common_symbols:
            matrix_sum = get_common_symbols_matrices(fa_graph, fa_rsm, common_symbols)
        else:
            matrix_sum = dok_matrix((num_states, num_states), dtype=bool)

        matrix_sum = update_matrix(matrix_sum, num_states)
        current_non_zeros = matrix_sum.count_nonzero()

        if current_non_zeros <= previous_non_zeros:
            break
        previous_non_zeros = current_non_zeros

        process_reachable_pairs(matrix_sum, state_mapping, fa_rsm, fa_graph)

    initial_symbol = rsm.initial_label.value
    if initial_symbol not in fa_graph.matrix:
        return set()

    result = set()
    for graph_from_state, graph_to_state in product(start_nodes, final_nodes):
        graph_from = fa_graph.states_to_states[graph_from_state]
        graph_to = fa_graph.states_to_states[graph_to_state]
        if fa_graph.matrix[initial_symbol][graph_from, graph_to]:
            result.add((graph_from_state, graph_to_state))

    return result


def initialize_state_mapping(fa_graph, fa_rsm):
    """
    Инициализирует отображение состояний графа и RSM.
    """
    return {i: state for i, state in enumerate(product(fa_graph.states, fa_rsm.states))}


def get_common_symbols_matrices(fa_graph, fa_rsm, common_symbols):
    """
    Вычисляет суммы кронекеровских произведений для общих символов.
    """
    return sum(
        kron(fa_graph.matrix[symbol], fa_rsm.matrix[symbol])
        for symbol in common_symbols
    )


def update_matrix(matrix_sum, num_states):
    """
    Обновляет матрицу суммированием с её квадратом для вычисления транзитивного замыкания.
    """
    matrix_sum += eye(num_states, dtype=bool)
    for _ in range(num_states):
        matrix_sum += matrix_sum @ matrix_sum
    return matrix_sum


def process_reachable_pairs(matrix_sum, state_mapping, fa_rsm, fa_graph):
    """
    Обрабатывает пары достижимых состояний и обновляет конечный автомат графа.
    """
    for from_idx, to_idx in zip(*matrix_sum.nonzero()):
        from_state, to_state = state_mapping[from_idx], state_mapping[to_idx]
        if from_state[1] in fa_rsm.start_states and to_state[1] in fa_rsm.final_states:
            symbol = from_state[1].value
            graph_from = fa_graph.states_to_states[from_state[0]]
            graph_to = fa_graph.states_to_states[to_state[0]]
            fa_graph.matrix.setdefault(
                symbol,
                dok_matrix((len(fa_graph.states), len(fa_graph.states)), dtype=bool),
            )[graph_from, graph_to] = True
