import scipy.sparse as sp
from networkx.classes import MultiDiGraph
from project.task2 import regex_to_dfa, graph_to_nfa
from project.task3 import AdjacencyMatrixFA


class MsBfsRpq:
    __matrices_type: type(sp.spmatrix)
    __adj_dfa: AdjacencyMatrixFA
    __adj_nfa: AdjacencyMatrixFA
    __start_nfa_states: list[int]
    __right_front: sp.spmatrix
    __dfa_size: int
    __nfa_size: int

    def __init__(self, adj_dfa: AdjacencyMatrixFA, adj_nfa: AdjacencyMatrixFA):
        self.__matrices_type = adj_dfa.matrix_type
        self.__adj_dfa = adj_dfa
        self.__adj_nfa = adj_nfa
        self.__dfa_size = adj_dfa.states_number
        self.__nfa_size = adj_nfa.states_number
        self.__start_nfa_states = list(adj_nfa.start_states)
        self.__united_symbols = set(self.__adj_dfa.symbol_matrices.keys()).intersection(
            self.__adj_nfa.symbol_matrices.keys()
        )
        self.__permutation_matrices = {
            symbol: sp.block_diag(
                [
                    adj_dfa.symbol_matrices[symbol].transpose()
                    for _ in self.__start_nfa_states
                ]
            )
            for symbol in self.__united_symbols
        }

    def __initialize_front(self):
        all_vectors = []

        for nfa_state in self.__start_nfa_states:
            vector = self.__matrices_type(
                (self.__dfa_size, self.__nfa_size), dtype=bool
            )
            for dfa_start in self.__adj_dfa.start_states:
                vector[dfa_start, nfa_state] = True
            all_vectors.append(vector)

        return self.__matrices_type(sp.vstack(all_vectors))

    def ms_bfs(self):
        new_front = self.__initialize_front()
        visited_fronts = new_front.copy()

        while new_front.count_nonzero():
            next_front = new_front.copy()
            for symbol in self.__united_symbols:
                next_front += self.__permutation_matrices[symbol] @ (
                    new_front @ self.__adj_nfa.symbol_matrices[symbol]
                )

            new_front = next_front > visited_fronts
            visited_fronts += new_front

        result = set()

        for left, nfa_state in zip(*visited_fronts.nonzero()):
            if (
                left % self.__dfa_size in self.__adj_dfa.final_states
                and nfa_state in self.__adj_nfa.final_states
            ):
                result.add(
                    (
                        self.__adj_nfa.int_to_states[
                            self.__start_nfa_states[left // self.__dfa_size]
                        ],
                        self.__adj_nfa.int_to_states[nfa_state],
                    )
                )

        return result


def ms_bfs_based_rpq(
    regex: str,
    graph: MultiDiGraph,
    start_nodes: set[int],
    final_nodes: set[int],
    matrix_type: type(sp.spmatrix) = sp.csr_matrix,
) -> set[tuple[int, int]]:
    return MsBfsRpq(
        AdjacencyMatrixFA(regex_to_dfa(regex), matrix_type=matrix_type),
        AdjacencyMatrixFA(
            graph_to_nfa(graph, start_nodes, final_nodes), matrix_type=matrix_type
        ),
    ).ms_bfs()
