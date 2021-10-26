from typing import Set, Iterable

import networkx as nx
from pyformlang.cfg import Variable
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
)
from pyformlang.regular_expression import Regex

__all__ = [
    "get_min_dfa_from_regex_str",
    "get_min_dfa_from_regex",
    "get_nfa_from_graph",
    "RSMBox",
    "RSM",
    "get_rsm_from_ecfg",
    "minimize_rsm",
    "check_regex_equality",
]

from project.grammar_tools import ECFG


def get_min_dfa_from_regex_str(regex_str: str) -> DeterministicFiniteAutomaton:
    """
    Based on a regular expression given as a Regex string, builds an Deterministic Finite Automaton.

    Parameters
    ----------
    regex_str: str
        The Regex string representation of a regular expression

    Returns
    -------
    DeterministicFiniteAutomaton
        Deterministic Finite Automaton equivalent to a given regular expression as a Regex string
    """

    return get_min_dfa_from_regex(Regex(regex_str))


def get_min_dfa_from_regex(regex: Regex) -> DeterministicFiniteAutomaton:
    """
    Based on a regular expression given as Regex, builds an Deterministic Finite Automaton.

    Parameters
    ----------
    regex: Regex
        The Regex representation of a regular expression

    Returns
    -------
    DeterministicFiniteAutomaton
        Deterministic Finite Automaton equivalent to a given regular expression as a Regex
    """

    e_nfa = regex.to_epsilon_nfa()
    min_dfa = e_nfa.minimize()

    return min_dfa


def get_nfa_from_graph(
    graph: nx.MultiDiGraph,
    start_node_nums: Set[int] = None,
    final_node_nums: Set[int] = None,
) -> NondeterministicFiniteAutomaton:
    """
    Generates an Nondeterministic Finite Automaton for a specified graph and start or final nodes.

    If start_nodes or final_nodes are not specified, all nodes are considered start or final respectively.

    Parameters
    ----------
    graph: nx.MultiDiGraph
        Graph to generating an Nondeterministic Finite Automaton from it
    start_node_nums: Set[int], default = None
        Set of start node numbers to configure Nondeterministic Finite Automaton,
        which must exist in the graph
    final_node_nums: Set[int], default = None
        Set of final node numbers to configure Nondeterministic Finite Automaton,
        which must exist in the graph

    Returns
    -------
    NondeterministicFiniteAutomaton
        Nondeterministic Finite Automaton equivalent to a specified graph

    Raises
    ------
    ValueError
        If non-existent in the specified graph node number is used
    """

    nums_nodes = dict()

    if graph.number_of_nodes() != 0:
        nums_nodes = {num: node for num, node in enumerate(graph.nodes)}

    start_nums_nodes = dict()
    final_nums_nodes = dict()

    if not start_node_nums:
        for num, node in nums_nodes.items():
            start_nums_nodes[num] = node
    else:
        if not start_node_nums.issubset(set(nums_nodes.keys())):
            raise ValueError(
                f"Non-existent start node numbers in the graph: "
                f"{start_node_nums.difference(set(nums_nodes.keys()))}"
            )

        for num in start_node_nums:
            start_nums_nodes[num] = nums_nodes[num]

    if not final_node_nums:
        for num, node in nums_nodes.items():
            final_nums_nodes[num] = node
    else:
        if not final_node_nums.issubset(set(nums_nodes.keys())):
            raise ValueError(
                f"Non-existent final node numbers in the graph: "
                f"{final_node_nums.difference(set(nums_nodes.keys()))}"
            )

        for num in final_node_nums:
            final_nums_nodes[num] = nums_nodes[num]

    nfa = NondeterministicFiniteAutomaton()

    for node in nums_nodes.values():
        nfa.states.add(State(node))

    for node_from, node_to in graph.edges():
        edge_label = graph.get_edge_data(node_from, node_to)[0]["label"]
        nfa.add_transition(node_from, edge_label, node_to)

    for num in start_nums_nodes.keys():
        start_state = list(nfa.states)[num]
        nfa.add_start_state(start_state)

    for num in final_nums_nodes.keys():
        final_state = list(nfa.states)[num]
        nfa.add_final_state(final_state)

    return nfa


class RSMBox:
    """
    A class encapsulates a box with DFA by RSM variable for Recursive State Machine.

    Parameters
    ----------
    variable: Variable
       Variable of RSM
    dfa: DeterministicFiniteAutomaton
        DFA by RSM variable
    """

    def __init__(
        self, variable: Variable = None, dfa: DeterministicFiniteAutomaton = None
    ):
        self._dfa = dfa
        self._variable = variable

    @property
    def dfa(self) -> DeterministicFiniteAutomaton:
        return self._dfa

    @property
    def variable(self) -> Variable:
        return self._variable

    def minimize(self) -> None:
        """
        Minimize Deterministic Finite Automaton in the RSMBox.

        Returns
        -------
        None
        """

        self._dfa = self._dfa.minimize()

    def __eq__(self, other: "RSMBox") -> bool:
        return self._variable == other._variable and self._dfa.is_equivalent_to(
            other._dfa
        )


class RSM:
    """
    A class encapsulates a Recursive State Machine.

    Parameters
    ----------
    start_symbol: Variable
        A start symbol for RSM
    boxes: Iterable[RSMBox]
        A collection of RSMBox with DFA by RSM variable
    """

    def __init__(
        self,
        start_symbol: Variable,
        boxes: Iterable[RSMBox],
    ):
        self._start_symbol = start_symbol
        self._boxes = boxes

    @property
    def start_symbol(self):
        return self._start_symbol

    @property
    def boxes(self):
        return self._boxes

    @start_symbol.setter
    def start_symbol(self, start_symbol: Variable):
        self._start_symbol = start_symbol

    def minimize(self) -> "RSM":
        """
        Minimize Recursive State Machine means minimize each
        Deterministic Finite Automaton in boxes.

        Returns
        -------
        RSM:
            Minimal RSM
        """

        for box in self._boxes:
            box.minimize()

        return self

    @classmethod
    def from_ecfg(cls, ecfg: ECFG) -> "RSM":
        """
        Converts an Extended Context Free Grammar to a Recursive State Machine.

        Returns
        -------
        RSM:
            RSM from ECFG
        """

        boxes = [
            RSMBox(production.head, get_min_dfa_from_regex(production.body))
            for production in ecfg.productions
        ]

        return cls(start_symbol=ecfg.start_symbol, boxes=boxes)


def minimize_rsm(rsm: RSM) -> RSM:
    """
    Minimize Recursive State Machine means minimize each
    Deterministic Finite Automaton in boxes.

    Returns
    -------
    RSM:
        Minimal RSM
    """

    return rsm.minimize()


def get_rsm_from_ecfg(ecfg: ECFG) -> RSM:
    """
    Converts an Extended Context Free Grammar to a Recursive State Machine.

    Returns
    -------
    RSM:
        RSM from ECFG
    """

    return RSM.from_ecfg(ecfg)


def check_regex_equality(regex1: Regex, regex2: Regex) -> bool:
    """
    Check whether Regex1 is equivalent to Regex2.
    It means their languages are equal.

    Parameters
    ----------
    regex1: Regex
        First regex
    regex2: Regex
        Second regex

    Returns
    -------
    bool:
        True if regex1 is equivalent to regex2
        False otherwise
    """

    return get_min_dfa_from_regex(regex1).is_equivalent_to(
        get_min_dfa_from_regex(regex2)
    )
