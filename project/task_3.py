import numpy as np
import scipy.sparse as sp
from project.automata_builder import get_nfa_from_graph
from networkx import MultiDiGraph

__all__ = [
    "FAMatrix",
    "matrix_from_fa_graph",
    "bool_dec",
    "kronecker",
    "intersect_finite_automata",
    "regex_path_in_automaton",
]


class FAMatrix:
    def __init__(self):
        self.matrix = []
        self.symbols = set()
        self.starts = set()
        self.finals = set()
        self.size = 0
        self.states = []

    def __init__(self, matrix, symbols, starts, finals, size, states):
        self.matrix = matrix
        self.symbols = symbols
        self.starts = starts
        self.finals = finals
        self.size = size
        self.states = states


def matrix_from_fa_graph(graph):
    edges = list(graph.edges(data="label", default="ɛ"))
    nodes = list(graph.nodes(data=True))

    starts, finals = set(), set()
    states = dict()
    index = 0

    for state in nodes:
        if not state[0] in states:
            states[state[0]] = index
            if "is_start" in state[1] and state[1]["is_start"]:
                starts.add(index)
            if "is_final" in state[1] and state[1]["is_final"]:
                finals.add(index)
            index += 1

    matrix = []
    size = index
    symbols = set()
    for i in range(size):
        matrix.append([set() for j in range(size)])

    for transition in edges:
        state_from = states[transition[0]]
        state_to = states[transition[1]]
        symbol = transition[2]
        matrix[state_from][state_to].add(symbol)
        symbols.add(symbol)

    state_from_number = [(0, 0)] * size

    for state in states:
        state_from_number[states[state]] = state

    return FAMatrix(matrix, symbols, starts, finals, size, state_from_number)


def bool_dec(matrix: FAMatrix):
    matrices = dict()

    for symbol in matrix.symbols:
        matrices[symbol] = sp.csr_matrix((matrix.size, matrix.size), dtype=bool)

    for state_from in range(matrix.size):
        for state_to in range(matrix.size):
            for symbol in matrix.matrix[state_from][state_to]:
                matrices[symbol][state_from, state_to] = True

    return matrices


def kronecker(matrixA: FAMatrix, matrixB: FAMatrix):
    size = matrixA.size * matrixB.size
    matrix = []
    for i in range(size):
        matrix.append([])
        for j in range(size):
            matrix[i].append(set())

    symbols = set()
    starts, finals = set(), set()

    decompositionA = bool_dec(matrixA)
    decompositionB = bool_dec(matrixB)

    for symbol in matrixA.symbols:
        symbols.add(symbol)
    for symbol in matrixB.symbols:
        symbols.add(symbol)

    for symbol in symbols:
        symbol_matrix = sp.kron(decompositionA[symbol], decompositionB[symbol]).tocsr()
        for state_from in range(size):
            for state_to in range(size):
                if symbol_matrix[state_from, state_to]:
                    matrix[state_from][state_to].add(symbol)

    for i in matrixA.starts:
        for j in matrixB.starts:
            starts.add(((i + 1) * (j + 1)) - 1)

    for i in matrixA.finals:
        for j in matrixB.finals:
            finals.add(((i + 1) * (j + 1)) - 1)

    states = [(0, 0)] * size

    for stateA in range(len(matrixA.states)):
        for stateB in range(len(matrixB.states)):
            states[stateA * matrixB.size + stateB] = (
                matrixA.states[stateA],
                matrixB.states[stateB],
            )

    # for i in range(len(states)):
    #     print(i, states[i])

    # for string in matrix:
    #     str_print = [i for i in string]
    #     print(*str_print)

    return FAMatrix(matrix, symbols, starts, finals, size, states)


def intersect_finite_automata(A, B):
    graphA = A.to_networkx()
    graphB = B.to_networkx()

    matrixA = matrix_from_fa_graph(graphA)
    matrixB = matrix_from_fa_graph(graphB)

    matrix = kronecker(matrixA, matrixB)

    graph = MultiDiGraph()
    graph.add_nodes_from(range(matrix.size))

    # print(matrix.size)
    # print(*[i for i in matrix.starts])
    # print(*[i for i in matrix.finals])

    for state_from in range(matrix.size):
        for state_to in range(matrix.size):
            for symbol in matrix.matrix[state_from][state_to]:
                graph.add_edge(state_from, state_to, label=symbol)
                # print(state_from, state_to, symbol)

    return get_nfa_from_graph(graph, matrix.starts, matrix.finals)


def csr_matrices_are_equal(A, B, size):
    answer = True
    for i in range(size):
        for j in range(size):
            if A[i, j] != B[i, j]:
                answer = False
                break
        if not answer:
            break
    return answer


def regex_path_in_automaton(regex, graph, starts, finals):
    regex_matrix = matrix_from_fa_graph(
        regex.to_epsilon_nfa().to_deterministic().to_networkx()
    )
    graph_nfa = get_nfa_from_graph(
        graph, starts, finals
    )  # to add start and final states
    graph_matrix = matrix_from_fa_graph(graph_nfa.to_networkx())
    matrix = kronecker(regex_matrix, graph_matrix)
    bool_matrix = sp.csr_matrix((matrix.size, matrix.size), dtype=bool)

    for state_from in range(matrix.size):
        for state_to in range(matrix.size):
            if matrix.matrix[state_from][state_to] == set():
                bool_matrix[state_from, state_to] = False
            else:
                bool_matrix[state_from, state_to] = True
            if state_from == state_to:
                bool_matrix[state_from, state_to] = True

    mul_matrix = bool_matrix * bool_matrix + bool_matrix

    while not csr_matrices_are_equal(mul_matrix, bool_matrix, matrix.size):
        bool_matrix = mul_matrix
        mul_matrix = bool_matrix * bool_matrix + bool_matrix

    answer = set()

    # print(graph_matrix.states)
    # print(regex_matrix.states)

    for state_from in range(matrix.size):
        for state_to in range(matrix.size):
            if mul_matrix[state_from, state_to]:
                regex_from, graph_from = matrix.states[state_from]
                regex_to, graph_to = matrix.states[state_to]

                regex_from_id, graph_from_id = (
                    state_from // graph_matrix.size,
                    state_from % graph_matrix.size,
                )
                regex_to_id, graph_to_id = (
                    state_to // graph_matrix.size,
                    state_to % graph_matrix.size,
                )

                if (
                    regex_from_id in regex_matrix.starts
                    and graph_from_id in graph_matrix.starts
                ):
                    if (
                        regex_to_id in regex_matrix.finals
                        and graph_to_id in graph_matrix.finals
                    ):
                        answer.add((graph_from, graph_to))
                        # print(graph_from_id, graph_to_id)

    return answer
