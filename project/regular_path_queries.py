
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, Symbol, State, EpsilonNFA
from scipy import sparse
from scipy.sparse import dok_matrix, kron, coo_matrix, csr_matrix
def decompose_fa(fa: EpsilonNFA) -> (dict[str, dok_matrix], dict[State, int]):
    """
    Decomposition of FA as a dictionary: key is symbol, value is transition matrix for x
    :param fa: finite automaton
    :return:
    """
    states = {state: idx for idx, state in enumerate(fa.states)}
    n_states = len(fa.states)

    result = {}

    for fr, label, to in fa:
        matrix = result.setdefault(label, sparse.dok_matrix((n_states, n_states), dtype=bool),)
        matrix[states[fr], states[to]] = True

    inds = list(fa.states)
    return result, states, inds


def intersect(fa1: EpsilonNFA, fa2: EpsilonNFA) -> EpsilonNFA:
    """
    Computes the intersection of two finite automata using tensor product

    Parameters
    ----------
    `fa1`: First finite automaton
    `fa2`: Second finite automaton

    Returns
    -------
    The intersection of two finite automatas
    """

    fa1_bool, fa1_states, inds1 = decompose_fa(fa1)
    fa2_bool, fa2_states, inds2 = decompose_fa(fa2)

    n_states1 = len(fa1_states)
    n_states2 = len(fa2_states)

    same_labels = set(fa1_bool.keys()).intersection(fa2_bool.keys())
    bool_decomposition = {label: dok_matrix(kron(fa1_bool[label], fa2_bool[label]))
                          for label in same_labels}

    result = EpsilonNFA()

    result_states = [None] * (n_states1 * n_states2)


    for i in range(n_states1):
        for j in range(n_states2):
            result_states[i * n_states2 + j] = State((inds1[i], inds2[j]))

    for l, mat in bool_decomposition.items():
        for (fr, to), value in mat.items():
            if value:
                result.add_transition(result_states[fr], l, result_states[to])

    for s1 in fa1.start_states:
        for s2 in fa2.start_states:
            result.add_start_state(result_states[fa1_states[s1] * n_states2 + fa2_states[s2]])

    for s1 in fa1.final_states:
        for s2 in fa2.final_states:
            result.add_final_state(result_states[fa1_states[s1] * n_states2 + fa2_states[s2]])

    return result

#  На основе предыдущей функции реализовать функцию выполнения регулярных запросов к графам:
#  по графу с заданными стартовыми и финальными вершинами и регулярному выражению вернуть те пары
#  вершин из заданных стартовых и финальных, которые связанны путём, формирующем слово из языка,
#  задаваемого регулярным выражением.
#
#     Для конструирования регулярного запроса и преобразований графа использовать результаты Задачи 2.


