from .task3 import *
from .task2 import *
from scipy.sparse import hstack
from scipy.sparse import dok_matrix
from scipy.sparse import block_diag
from collections import defaultdict


def diagonalize_ones_matrix(matrix: dok_matrix, m: int) -> dok_matrix:
    if matrix is None:
        return matrix
    matrix = matrix.toarray()
    g = np.zeros(shape=matrix.shape, dtype=matrix.dtype)
    for i in range(matrix.shape[0] // m):
        for j in range(m):
            g[i * m + j] = matrix[i * m : i * m + m][
                matrix[i * m : i * m + m, j] > 0
            ].sum(axis=0)
    return dok_matrix(g)


def reachability_with_constraints(
    fa: FiniteAutomaton, constraints_fa: FiniteAutomaton
) -> dict[int, set[int]]:

    main = fa.get_matrix_word()
    constraints = constraints_fa.get_matrix_word()

    st_states_fa = fa.get_start_states()
    st_states_constraints_fa = constraints_fa.get_start_states()

    m = fa.get_n_states()
    n = constraints_fa.get_n_states()

    result = defaultdict(lambda: set())

    for sti in st_states_fa:

        if sti in fa.final_states:
            for i in constraints_fa.start_states:
                if i in constraints_fa.final_states:
                    result[fa.map_to_id[sti]].add(fa.map_to_id[sti])

        F = dok_matrix((n, m + n), dtype=np.bool_)

        for stj in st_states_constraints_fa:
            F[stj, stj] = True
        F[:, n + sti] = True

        for _ in range(m * n):
            res = None
            for word in main:
                if word not in constraints:
                    continue

                M_work = block_diag((constraints[word], main[word]))
                F_next = diagonalize_ones_matrix(F @ M_work, n)
                if res is None:
                    res = F_next
                else:
                    res += F_next
            if res is None:
                break
            F = res

            for stifinal in constraints_fa.get_final_states():
                if F[stifinal, stifinal] == 0:
                    continue

                for stjfinal in fa.get_final_states():
                    if F[stifinal, n + stjfinal] > 0:
                        result[fa.map_from_id[sti]].add(fa.map_from_id[stjfinal])
    return result
