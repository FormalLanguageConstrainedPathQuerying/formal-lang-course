from typing import Iterable, Dict, Set, Tuple, List, Union
from networkx import MultiDiGraph
from pyformlang.cfg import Epsilon
from pyformlang.finite_automaton import Symbol, State, NondeterministicFiniteAutomaton
from pyformlang.rsa import RecursiveAutomaton
from scipy.sparse import dok_matrix, kron
from project.task2.fa_builders import regex_to_dfa, graph_to_nfa


class FiniteAutomaton:
    """
    Конечный автомат
    """

    def __init__(
        self,
        nfa: NondeterministicFiniteAutomaton = None,
        *,
        start_states: Set[State] = None,
        final_states: Set[State] = None,
        matrix: Dict[Symbol, dok_matrix] = None,
        states_to_states: Dict[State, int] = None,
        is_from_rsm: bool = False,
        eps: Set[Symbol] = None,
        states: Set[State] = None
    ):
        """
        Аргументы:
            start_states (Set[State], optional): Начальные состояния автомата
            final_states (Set[State], optional): Конечные состояния автомата
            states_to_states (Dict[State, int], optional): Отображение состояний на их числовые индексы
            eps (Set[Symbol], optional): Набор эпсилон-переходов
            matrix (Dict[Symbol, dok_matrix], optional): Словарь, представляющий переходы состояний
            nfa (NondeterministicFiniteAutomaton, optional): НКА для инициализации конечного автомата
        """
        self.nfa = nfa
        self.start_states = start_states
        self.final_states = final_states
        self.states_to_states = states_to_states
        self.eps = eps
        self.lbl = True
        self.matrix = matrix

        if nfa is None:
            if not is_from_rsm:
                self.nfa = to_nfa(self)
            self.states = states
        else:
            self.states_to_states = {v: i for i, v in enumerate(nfa.states)}
            self.matrix = nfa_to_matrix(nfa, self.states_to_states)
            self.start_states = nfa.start_states
            self.final_states = nfa.final_states
            self.states = list(nfa.states)

    def accepts(self, word: Iterable[Symbol]) -> bool:
        return self.nfa.accepts(word)

    def is_empty(self) -> bool:
        return self.nfa.is_empty()

    def size(self) -> int:
        return len(self.states_to_states)

    def mapping_for(self, u: State) -> int:
        return self.states_to_states[u]

    def start_indices(self) -> List[int]:
        return [self.mapping_for(t) for t in self.start_states]

    def final_indices(self) -> List[int]:
        return [self.mapping_for(t) for t in self.final_states]

    def labels(self) -> Iterable[Symbol]:
        return self.states_to_states.keys() if self.lbl else self.matrix.keys()

    def revert_mapping(self) -> Dict[int, State]:
        return {i: v for v, i in self.states_to_states.items()}


def to_set(state: Union[State, Set[State]]) -> Set[State]:
    if not isinstance(state, set):
        return {state}
    return state


def nfa_to_matrix(
    nfa: NondeterministicFiniteAutomaton, states: Dict[State, int]
) -> Dict[Symbol, dok_matrix]:
    len_states = len(nfa.states)
    result = {
        symbol: dok_matrix((len_states, len_states), dtype=bool)
        for symbol in nfa.symbols
    }

    for v, edges in nfa.to_dict().items():
        for symbol, targets in edges.items():
            for u in to_set(targets):
                result[symbol][states[v], states[u]] = True

    return result


def rsm_to_fa(rsm: RecursiveAutomaton) -> FiniteAutomaton:
    states, start_states, final_states, epsilons = set(), set(), set(), set()

    for label, enfa in rsm.boxes.items():
        for state in enfa.dfa.states:
            s = State((label, state.value))
            states.add(s)
            if state in enfa.dfa.start_states:
                start_states.add(s)
            if state in enfa.dfa.final_states:
                final_states.add(s)

    len_states = len(states)
    states_to_int = {s: i for i, s in enumerate(states)}

    matrix = {}
    for label, enfa in rsm.boxes.items():
        for frm, transition in enfa.dfa.to_dict().items():
            for symbol, to in transition.items():
                if symbol not in matrix:
                    matrix[symbol.value] = dok_matrix(
                        (len_states, len_states), dtype=bool
                    )
                for target in to_set(to):
                    matrix[symbol.value][
                        states_to_int[State((label, frm.value))],
                        states_to_int[State((label, target.value))],
                    ] = True
                if isinstance(to, Epsilon):
                    epsilons.add(label)

    return FiniteAutomaton(
        nfa=None,
        matrix=matrix,
        start_states=start_states,
        final_states=final_states,
        states_to_states=states_to_int,
        is_from_rsm=True,
        eps=epsilons,
        states=states,
    )


def to_nfa(fa: FiniteAutomaton) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()

    for symbol, matrix in fa.matrix.items():
        matrix_size = matrix.shape[0]
        for u in range(matrix_size):
            for v in range(matrix_size):
                if matrix[u, v]:
                    nfa.add_transition(
                        State(fa.revert_mapping()[u]),
                        symbol,
                        State(fa.revert_mapping()[v]),
                    )

    for state in fa.start_states:
        nfa.add_start_state(State(fa.revert_mapping()[fa.states_to_states[state]]))
    for state in fa.final_states:
        nfa.add_final_state(State(fa.revert_mapping()[fa.states_to_states[state]]))

    return nfa


def intersect_automata(
    fa1: FiniteAutomaton, fa2: FiniteAutomaton, lbl: bool = True
) -> FiniteAutomaton:
    fa1.lbl = fa2.lbl = not lbl
    labels = set(fa1.labels()) & set(fa2.labels())
    matrix = {
        label: kron(fa1.matrix[label], fa2.matrix[label], "csr") for label in labels
    }

    start_states, final_states, states_to_int = set(), set(), {}

    for u, i in fa1.states_to_states.items():
        for v, j in fa2.states_to_states.items():
            k = len(fa2.states_to_states) * i + j
            states_to_int[k] = k

            if u in fa1.start_states and v in fa2.start_states:
                start_states.add(State(k))

            if u in fa1.final_states and v in fa2.final_states:
                final_states.add(State(k))

    return FiniteAutomaton(
        nfa=None,
        matrix=matrix,
        start_states=start_states,
        final_states=final_states,
        states_to_states=states_to_int,
    )


def transitive_closure(fa: FiniteAutomaton) -> dok_matrix:
    if not fa.matrix:
        return dok_matrix((0, 0), dtype=bool)

    front = sum(fa.matrix.values())
    prev_count = 0

    while front.count_nonzero() != prev_count:
        prev_count = front.count_nonzero()
        front += front @ front

    return front


def paths_ends(
    graph: MultiDiGraph, start_nodes: Set[int], final_nodes: Set[int], regex: str
) -> List[Tuple[object, object]]:
    g_fa = FiniteAutomaton(graph_to_nfa(graph, start_nodes, final_nodes))
    r_fa = FiniteAutomaton(regex_to_dfa(regex))
    inters_fa = intersect_automata(g_fa, r_fa, lbl=False)
    closure = transitive_closure(inters_fa)
    size = len(r_fa.states_to_states)

    return [
        (g_fa.revert_mapping()[v // size], g_fa.revert_mapping()[u // size])
        for v, u in zip(*closure.nonzero())
        if State(v) in inters_fa.start_states and State(u) in inters_fa.final_states
    ]
