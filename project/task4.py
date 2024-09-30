import scipy.sparse as sp
from collections import defaultdict
from itertools import product
from networkx.classes import MultiDiGraph
from project.task2 import regex_to_dfa, graph_to_nfa
from project.task3 import AdjacencyMatrixFA, intersect_automata


class MsBfsRpq:
    def __init__(self, adj_dfa: AdjacencyMatrixFA, adj_nfa: AdjacencyMatrixFA):
        self.__adj_dfa = adj_dfa
        self.__adj_nfa = adj_nfa
        self.__dfa_size = adj_dfa.states_number
        self.__nfa_size = adj_nfa.states_number
        self.__start_nfa_states = list(adj_nfa.start_states)
        self.__united_adj_matrix = {
            symbol: sp.block_diag(
                [adj_dfa.symbol_matrices[symbol], adj_nfa.symbol_matrices[symbol]]
            )
            for symbol in intersect_automata(adj_dfa, adj_nfa).symbol_matrices.keys()
        }
        self.__left_front, self.__right_front = self.__initialize_fronts()

    def __initialize_fronts(self) -> (sp.spmatrix, sp.spmatrix):
        identity_matrix = sp.identity(self.__dfa_size, dtype=bool)
        all_vectors = []

        for nfa_state in self.__start_nfa_states:
            vector = sp.lil_matrix((self.__dfa_size, self.__nfa_size), dtype=bool)
            for dfa_start in self.__adj_dfa.start_states:
                vector[dfa_start, nfa_state] = True
            all_vectors.append(sp.hstack([identity_matrix, vector]))

        combined_vectors = sp.vstack(all_vectors).tocsr()
        return combined_vectors[:, : self.__dfa_size], combined_vectors[
            :, self.__dfa_size :
        ]

    def ms_bfs(self) -> dict[int, set[int]]:
        def multiply(front, matrix, shape):
            result = front @ matrix
            updated = sp.lil_matrix(shape, dtype=bool)

            for i, j in zip(*result[:, : self.__dfa_size].nonzero()):
                updated[i // self.__dfa_size * self.__dfa_size + j, :] += result[
                    i, self.__dfa_size :
                ]

            return updated

        new_front = sp.lil_matrix(self.__right_front, dtype=bool)
        visited_fronts = sp.csr_matrix(new_front, dtype=bool)

        while new_front.count_nonzero():
            combined_front = sp.hstack([self.__left_front, new_front])
            new_front = sum(
                multiply(combined_front, matrix, new_front.shape)
                for matrix in self.__united_adj_matrix.values()
            )
            new_front = new_front > visited_fronts
            visited_fronts += new_front

        result_dict = defaultdict(set)

        for start_idx, final_dfa_state in product(
            range(len(self.__start_nfa_states)), self.__adj_dfa.final_states
        ):
            reachable = set(
                visited_fronts[
                    start_idx * self.__dfa_size + final_dfa_state, :
                ].nonzero()[1]
            )
            result_dict[self.__start_nfa_states[start_idx]].update(reachable)

        return result_dict


def ms_bfs_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    regex_dfa = regex_to_dfa(regex)
    adj_dfa = AdjacencyMatrixFA(regex_dfa)
    graph_nfa = graph_to_nfa(graph, start_nodes, final_nodes)
    adj_nfa = AdjacencyMatrixFA(graph_nfa)

    bfs_result = MsBfsRpq(adj_dfa, adj_nfa).ms_bfs()

    return {
        (start, final)
        for start, final in product(graph_nfa.start_states, graph_nfa.final_states)
        if adj_nfa.states_to_int[final] in bfs_result[adj_nfa.states_to_int[start]]
    }
