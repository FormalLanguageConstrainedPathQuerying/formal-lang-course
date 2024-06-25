from scipy.sparse import block_diag, dok_matrix
from project.task3 import FiniteAutomaton


def diagonalise(m):
    res = dok_matrix(m.shape, dtype=bool)
    for i in range(m.shape[0]):
        for j in range(m.shape[0]):
            if m[j, i]:
                res[i] += m[j]
    return res


def reachability_with_constraints(
    fa: FiniteAutomaton, constraints_fa: FiniteAutomaton
) -> dict[int, set[int]]:
    matrices = {}
    len_con, len_fa = len(constraints_fa.states), len(fa.states)
    for line in fa.matrix.keys() & constraints_fa.matrix.keys():
        A = constraints_fa.matrix[line]
        B = fa.matrix[line]
        matrices[line] = block_diag((A, B))

    result = dict()
    for start in fa.states:
        result[start] = set()

    con_start_states = {
        constraints_fa.states_to_int[i] for i in constraints_fa.start_states
    }
    con_final_states = {
        constraints_fa.states_to_int[i] for i in constraints_fa.final_states
    }
    fa_start_states = {fa.states_to_int[i] for i in fa.start_states}
    fa_final_states = {fa.states_to_int[i] for i in fa.final_states}

    for state in fa_start_states:
        front = dok_matrix((len_con, len_con + len_fa), dtype=bool)
        for cst in con_start_states:
            front[cst, cst] = True

        for i in range(len_con):
            front[i, state + len_con] = True

        if state in fa_final_states:
            for i in con_start_states:
                if i in con_final_states:
                    result[fa.states[state]].add(fa.states[state])

        for _ in range(len_con * len_fa):
            new_front = dok_matrix((len_con, len_con + len_fa), dtype=bool)
            for line in fa.matrix.keys() & constraints_fa.matrix.keys():
                new_front += diagonalise(front @ matrices[line])
            front = new_front
            for i in range(len_con):
                if i in con_final_states and front[i, i]:
                    for j in range(len_fa):
                        if j in fa_final_states and front[i, j + len_con]:
                            result[fa.states[state]].add(fa.states[j])
    return result
