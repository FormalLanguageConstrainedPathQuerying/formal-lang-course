from project.task03 import FiniteAutomaton
from scipy.sparse import csr_matrix, block_diag


def bfs_front(m):
    h = m.shape[0]
    res = csr_matrix(m.shape, dtype=bool)
    for i in range(h):
        for j in range(h):
            if m[j, i]:
                res[i] += m[j]
    return res


def reachability_with_constraints(
    fa: FiniteAutomaton, constraints_fa: FiniteAutomaton
) -> dict[int, set[int]]:

    matrices = {}

    labels = fa.matrix.keys() & constraints_fa.matrix.keys()
    m, n = len(constraints_fa.int_map), len(fa.int_map)

    for label in labels:
        matrices[label] = block_diag((constraints_fa.matrix[label], fa.matrix[label]))

    height = m
    width = m + n

    res = {s.value: set() for s in fa.int_map}

    fa_start_states = fa.start_indices()
    fa_final_states = fa.final_indices()
    cfa_start_states = constraints_fa.start_indices()
    cfa_final_states = constraints_fa.final_indices()

    for start in fa_start_states:
        front = csr_matrix((height, width), dtype=bool)

        for constraint in cfa_start_states:
            front[constraint, constraint] = True

        for i in range(height):
            front[i, start + m] = True

        if start in fa_final_states:
            for i in cfa_start_states:
                if i in cfa_final_states:
                    res[fa.int_map[start]].add(fa.int_map[start])
                    break

        for _ in range(m * n):
            new_front = csr_matrix((height, width), dtype=bool)
            for label in labels:
                new_front += bfs_front(front @ matrices[label])
            front = new_front

            for i in range(height):
                if i in cfa_final_states and front[i, i]:
                    for j in range(n):
                        if j in fa_final_states and front[i, j + m]:
                            res[fa.int_map[start]].add(fa.int_map[j])
    return res
