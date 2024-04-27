from scipy.sparse import dok_matrix, block_diag

from project.task3 import FiniteAutomaton


def reachability_with_constraints(
    fa: FiniteAutomaton, constraints_fa: FiniteAutomaton
) -> dict[int, set[int]]:
    m, n = constraints_fa.size(), fa.size()

    def get_front(s):
        front = dok_matrix((m, m + n), dtype=bool)
        for i in constraints_fa.start_idxs():
            front[i, i] = True
        for i in range(m):
            front[i, s + m] = True
        return front

    def diag(mat):
        result = dok_matrix(mat.shape, dtype=bool)
        for i in range(mat.shape[0]):
            for j in range(mat.shape[0]):
                if mat[j, i]:
                    result[i] += mat[j]
        return result

    labels = fa.labels() & constraints_fa.labels()
    result = {s: set() for s in fa.start_states}
    adj = {
        label: block_diag((constraints_fa.basa[label], fa.basa[label]))
        for label in labels
    }

    for v in fa.start_idxs():
        front = get_front(v)
        last_ = -1
        for _ in range(m * n):
            front = sum(
                [dok_matrix((m, m + n), dtype=bool)]
                + [diag(front @ adj[label]) for label in labels]
            )
            fr = front[:, m:].nonzero()
            for a, b in zip(fr[0], fr[1]):
                if a in constraints_fa.final_idxs() and b in fa.final_idxs():
                    result[v].add(b)
                if hash(str(fr)) == last_:
                    break
                last_ = hash(str(fr))

    return result
