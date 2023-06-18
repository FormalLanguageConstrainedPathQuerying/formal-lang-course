from itertools import product
from typing import NamedTuple, Any

import networkx as nx
import scipy.sparse as sp
from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable
from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    Symbol,
    EpsilonNFA,
)
from scipy.sparse import dok_array, csr_array, eye, block_diag

from project.finite_automata_converters import FAConverters
from project.matrix_cfpq import matrix_algorithm
from project.hellings import hellings


class TensorNFA:
    class State(NamedTuple):
        state_datum: Any
        is_start: bool
        is_finish: bool

    def __init__(
        self,
        matrix_dict: dict,
        shape=(0, 0),
        states_map: None | dict[int, State] = None,
    ):
        if states_map is None:
            states_map = {}
        self.matrix_dict = matrix_dict
        self.shape = shape
        self.states_map: dict[int, TensorNFA.State] = states_map

    def symbols(self):
        """
        @return: symbols of TensorNFA
        """
        return set(self.matrix_dict.keys())

    def __getitem__(self, symbol) -> sp.csr_matrix:
        return self.matrix_dict[symbol]

    @staticmethod
    def from_nfa(nfa: NondeterministicFiniteAutomaton):
        """
        Converts NondeterministicFiniteAutomaton to TensorNFA
        @param nfa: input NondeterministicFiniteAutomaton
        @return: corresponding TensorNFA
        """
        dok_matrix_dict: dict[str, sp.dok_matrix] = {}
        matrix_dict: dict[str, sp.csr_matrix] = {}
        shape = (len(nfa.states), len(nfa.states))

        states = set(
            TensorNFA.State(st.value, st in nfa.start_states, st in nfa.final_states)
            for st in nfa.states
        )
        states = sorted(states, key=lambda st: st.state_datum)

        states_map = {}
        for i, s in enumerate(states):
            states_map[i] = s

        d = nfa.to_dict()
        for u in d:
            for symbol_value, v_iter in d[u].items():
                dok = dok_matrix_dict.setdefault(
                    symbol_value.value, dok_array(shape, dtype=bool)
                )
                ui = next(i for i, s in states_map.items() if s.state_datum == u)
                for v in v_iter if isinstance(v_iter, set) else {v_iter}:
                    dok[
                        ui, next(i for i, s in states_map.items() if s.state_datum == v)
                    ] = True

        for symbol_value in dok_matrix_dict:
            matrix_dict[symbol_value] = dok_matrix_dict[symbol_value].tocsc()
        return TensorNFA(matrix_dict, shape, states_map)

    def to_nfa(self) -> NondeterministicFiniteAutomaton:
        """
        Converts to NondeterministicFiniteAutomaton
        @return: corresponding NondeterministicFiniteAutomaton
        """
        result = NondeterministicFiniteAutomaton()
        for state in self.states_map.values():
            if state.is_start:
                result.add_start_state(state.state_datum)
            if state.is_finish:
                result.add_final_state(state.state_datum)

        for symbol in self.matrix_dict:
            matrix: sp.dok_matrix = self.matrix_dict[symbol].todok()
            for (u, v) in matrix.keys():
                result.add_transition(
                    self.states_map[u].state_datum,
                    Symbol(symbol),
                    self.states_map[v].state_datum,
                )
        return result

    def intersect(self, other: "TensorNFA") -> "TensorNFA":
        """
        Find intersection of TensorNFA via kronecker product of its sparse matrices.
        @param other: TensorNFA to intersect
        @return: result TensorNFA
        """
        result_shape = (self.shape[0] * other.shape[0], self.shape[1] * other.shape[1])
        result_matrix_dict: dict[str, sp.csr_matrix] = {}

        states = [
            TensorNFA.State(
                (st1.state_datum, st2.state_datum),
                st1.is_start and st2.is_start,
                st1.is_finish and st2.is_finish,
            )
            for st1, st2 in product(self.states_map.values(), other.states_map.values())
        ]

        states_map = {}
        for i, s in enumerate(states):
            states_map[i] = s

        for symbol in self.symbols().union(other.symbols()):
            if symbol in self.symbols() and symbol in other.symbols():
                result_matrix_dict[symbol] = sp.kron(
                    self[symbol], other[symbol], format="csr"
                )
            else:
                result_matrix_dict[symbol] = csr_array(result_shape, dtype=bool)

        return TensorNFA(result_matrix_dict, result_shape, states_map)

    def block_diag(self, other: "TensorNFA") -> "TensorNFA":
        """
        Creates new TensorNFA with building a
        block diagonal sparse matrix from provided matrices.
        @param other: TensorNFA to diagonalizing append
        @return: resulted TensorNFA
        """
        result_shape = (self.shape[0] + other.shape[0], self.shape[1] + other.shape[1])

        result_states_map = {}
        for i, s in self.states_map.items():
            result_states_map[i] = s
        for i, s in other.states_map.items():
            result_states_map[i + len(self.states_map)] = s

        result_matrix_dict = {
            s: block_diag((self[s], other[s]), format="csc")
            for s in self.symbols().intersection(other.symbols())
        }

        return TensorNFA(result_matrix_dict, result_shape, result_states_map)

    def evaluate_step(self, front: sp.csr_matrix) -> sp.csr_matrix:
        rows, columns = front.shape
        new_front = eye(rows, columns, dtype=bool, format="dok")
        for matrix in self.matrix_dict.values():
            mult = front @ matrix
            nz = mult.nonzero()
            for i, j in list(zip(nz[0], nz[1])):
                if j < rows:
                    new_front[j, rows:] += mult[i, rows:]
        return new_front.tocsr()


def intersection_of_finite_automata_with_tensor_mult(
    nfa1: NondeterministicFiniteAutomaton, nfa2: NondeterministicFiniteAutomaton
) -> NondeterministicFiniteAutomaton:
    """
    Find intersection of two NondeterministicFiniteAutomaton via kronecker product of its sparse matrices.
    @param nfa1: first NondeterministicFiniteAutomaton
    @param nfa2: second NondeterministicFiniteAutomaton
    @return: intersection of nfa1 and nfa2
    """
    a = TensorNFA.from_nfa(nfa1)
    b = TensorNFA.from_nfa(nfa2)
    return a.intersect(b).to_nfa()


def query_to_graph_with_kronecker_mult(
    graph: MultiDiGraph, start_nodes, finish_nodes, regex_str: str
):
    """
    Querying regex to graph with start and finish nodes.
    Find out pairs of connected nodes.
    @param graph: graph to query with regex
    @param start_nodes: nodes in graph marked as start
    @param finish_nodes: nodes in graph marked as finish
    @param regex_str: regex string to query to graph
    @return: pairs of start and finish nodes connected with path in result of querying
    """
    regex_min_dfa = FAConverters.regex_to_min_dfa(regex_str)
    intersect = intersection_of_finite_automata_with_tensor_mult(
        FAConverters.graph_to_nfa(graph, start_nodes, finish_nodes), regex_min_dfa
    )
    answer = set()
    net = intersect.to_networkx()
    for s in intersect.start_states:
        for f in intersect.final_states:
            if nx.has_path(net, source=s, target=f):
                answer.add((s.value[0], f.value[0]))
    return answer


def _find_accessible_nodes(
    graph_tensor_dfa: TensorNFA, start_nodes, regex_tensor_dfa: TensorNFA
) -> set:
    """
    Solve restricted RPQ with multiplying adjacency matrices to frontier nodes set.
    @param graph_tensor_dfa: graph to querying to.
    @param start_nodes: start nodes of graph_tensor_dfa.
    @param regex_tensor_dfa: regex graph.
    @return: set of graph_tensor_dfa accessible nodes from start_nodes with regex_tensor_dfa.
    """
    start_indexes = set()
    for i, s in graph_tensor_dfa.states_map.items():
        if s.state_datum in start_nodes:
            start_indexes.add(i)

    diagonal_graph = regex_tensor_dfa.block_diag(graph_tensor_dfa)

    rows = regex_tensor_dfa.shape[0]
    columns = rows + graph_tensor_dfa.shape[0]

    states = eye(rows, columns, dtype=bool, format="dok")
    for index, start_state in filter(
        lambda i_s: i_s[1].is_start, regex_tensor_dfa.states_map.items()
    ):
        for gs in start_indexes:
            states[index, rows + gs] = True

    prev_count_nonzero = 0
    front = states.tocsr()
    while states.count_nonzero() != prev_count_nonzero:
        prev_count_nonzero = states.count_nonzero()
        front = diagonal_graph.evaluate_step(front)
        states += front

    result = set()
    for finish_regex_index, finish_regex_state in filter(
        lambda i_s: i_s[1].is_finish, regex_tensor_dfa.states_map.items()
    ):
        for i in range(graph_tensor_dfa.shape[0]):
            if states[finish_regex_index, rows + i]:
                result.add(graph_tensor_dfa.states_map[i].state_datum)
    return result


def find_accessible_nodes(graph: MultiDiGraph, start_nodes, regex_str: str) -> set:
    """
    Find accessible nodes of graph with start_nodes and regex.
    @param graph: MultiDiGraph querying to.
    @param start_nodes: start nodes in graph.
    @param regex_str: regex for querying with to graph.
    @return: set of accessible nodes from any of start nodes satisfying regex.
    """
    regex_tensor_dfa = TensorNFA.from_nfa(FAConverters.regex_to_min_dfa(regex_str))
    graph_tensor_dfa = TensorNFA.from_nfa(FAConverters.graph_to_nfa(graph))
    return _find_accessible_nodes(graph_tensor_dfa, start_nodes, regex_tensor_dfa)


def find_accessible_nodes_of_nfa(nfa: EpsilonNFA, regex_str: str) -> set:
    """
    Find accessible nodes of graph with start_nodes and regex.
    @param nfa: EpsilonNFA querying to
    @param regex_str: regex for querying with to graph.
    @return: set of accessible nodes from any of start nodes satisfying regex.
    """
    regex_tensor_dfa = TensorNFA.from_nfa(FAConverters.regex_to_min_dfa(regex_str))
    graph_tensor_dfa = TensorNFA.from_nfa(nfa.to_deterministic())
    return _find_accessible_nodes(graph_tensor_dfa, nfa.start_states, regex_tensor_dfa)


def find_accessible_nodes_foreach_start(
    graph: MultiDiGraph, start_nodes, regex_str: str
) -> dict:
    """
    Find out dict of accessible nodes of graph and regex for each of start_nodes.
    @param graph: MultiDiGraph querying to.
    @param start_nodes: start nodes in graph.
    @param regex_str: regex for querying with to graph.
    @return: dict of accessible nodes from each of start nodes satisfying regex.
    """
    regex_tensor_dfa = TensorNFA.from_nfa(FAConverters.regex_to_min_dfa(regex_str))
    graph_tensor_dfa = TensorNFA.from_nfa(FAConverters.graph_to_nfa(graph))
    result_dict = dict()
    for sn in start_nodes:
        result_dict[sn] = _find_accessible_nodes(
            graph_tensor_dfa, {sn}, regex_tensor_dfa
        )
    return result_dict


def query_to_graph_from_any_starts(
    graph: MultiDiGraph, start_nodes, finish_nodes, regex_str: str
) -> set:
    """
    Querying regex to graph with start and finish nodes.
    Find out set of accessible nodes from starts.
    @param graph: graph to query with regex.
    @param start_nodes: nodes in graph marked as start.
    @param finish_nodes: nodes in graph marked as finish.
    @param regex_str: regex string to query to graph.
    @return: set of accessible finish nodes.
    """
    return find_accessible_nodes(graph, start_nodes, regex_str).intersection(
        set(finish_nodes)
    )


def query_to_graph_from_each_starts(
    graph: MultiDiGraph, start_nodes, finish_nodes, regex_str: str
) -> dict[set]:
    """
    Querying regex to graph with start and finish nodes.
    Find out dict of accessible nodes from each of starts nodes.
    @param graph: graph to query with regex.
    @param start_nodes: nodes in graph marked as start.
    @param finish_nodes: nodes in graph marked as finish.
    @param regex_str: regex string to query to graph.
    @return: dict of set of accessible finish nodes for each of starts nodes.
    """
    result = find_accessible_nodes_foreach_start(graph, start_nodes, regex_str)
    for i in result:
        result[i] = set(filter(lambda node: node in finish_nodes, result[i]))
    return result


def query_to_graph_with_matrix_algorithm(
    graph: nx.MultiDiGraph,
    cfg: str | CFG,
    start_var: str | Variable = Variable("S"),
    start_nodes: set[object] | None = None,
    final_nodes: set[object] | None = None,
) -> set[tuple[object, object]]:
    """
    Context free path querying by Matrix algorithm with restrictions
    @param graph: graph for querying
    @param cfg: context free grammar
    @param start_var: start Variable of grammar
    @param start_nodes: start nodes of graph
    @param final_nodes: finale nodes of graph
    @return: set of accessible pair of nodes:  {(Node, Node)}
    """
    if isinstance(start_var, str):
        start_var = Variable(start_var)
    if not isinstance(cfg, CFG):
        cfg = CFG.from_text(cfg, start_symbol=start_var)

    res = set()
    for start, var, final in matrix_algorithm(cfg, graph):
        if (
            var == start_var
            and (start_nodes is None or start in start_nodes)
            and (final_nodes is None or final in final_nodes)
        ):
            res.add((start, final))

    return res


def query_to_graph_with_hellings(
    graph: nx.MultiDiGraph,
    cfg: str | CFG,
    start_var: str | Variable = Variable("S"),
    start_nodes: set[object] | None = None,
    final_nodes: set[object] | None = None,
) -> set[tuple[object, object]]:
    """
    Context free path querying by Hellings algorithm with restrictions
    @param graph: graph for querying
    @param cfg: context free grammar
    @param start_var: start Variable of grammar
    @param start_nodes: start nodes of graph
    @param final_nodes: finale nodes of graph
    @return: set of accessible pair of nodes:  {(Node, Node)}
    """
    if isinstance(start_var, str):
        start_var = Variable(start_var)
    if not isinstance(cfg, CFG):
        cfg = CFG.from_text(cfg, start_symbol=start_var)

    res = set()
    for start, var, final in hellings(cfg, graph):
        if (
            var == start_var
            and (start_nodes is None or start in start_nodes)
            and (final_nodes is None or final in final_nodes)
        ):
            res.add((start, final))

    return res
