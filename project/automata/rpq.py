from project.automata.bool_matrix import BoolMatrix
from project.automata.builders import *


def rpq(
    regex: Regex,
    graph: MultiDiGraph,
    start_nodes: set[Hashable] = None,
    final_nodes: set[Hashable] = None,
) -> set[tuple[Hashable, Hashable]]:
    """
    Returns those pairs of nodes from the given graph with the given
    starting and final nodes and regular expression that are connected
    by path that forms a word from regular expression

    Parameters
    ----------
    regex : pyformlang.regular_expression.Regex
        The regular expression

    graph : networkx.MultiDiGraph
        The graph representation of the automaton

    start_nodes : set[Hashable], optional
        A finite set of start states - graph nodes

    final_nodes : set[Hashable], optional
        A finite set of final states - graph nodes

    Returns
    -------
    result : set[tuple[Hashable, Hashable]]
        A finite set of tuples with start and final nodes

    """
    nfa = build_nfa(graph, start_nodes, final_nodes)
    dfa = build_minimal_dfa(regex)

    nfa_bm = BoolMatrix(nfa)
    dfa_bm = BoolMatrix(dfa)

    intersected_automatas = nfa_bm.intersect(dfa_bm)

    closure = intersected_automatas.transitive_closure()

    index_to_states = {i: name for name, i in intersected_automatas.states.items()}

    return {
        (index_to_states[start_state][0], index_to_states[finish_state][0])
        for start_state, finish_state in zip(*closure.nonzero())
        if index_to_states[start_state][0] in nfa.start_states
        and index_to_states[finish_state][0] in nfa.final_states
    }


def bfs_rpq(
    regex: Regex,
    graph: MultiDiGraph,
    start_nodes: set[Hashable] = None,
    final_nodes: set[Hashable] = None,
    separate_flag: bool = False,
) -> set[Hashable]:
    """Responds to range path query with the specified mode:
    separated (for every start state), not separated (for all start state)

    Parameters
    ----------
    regex : pyformlang.regular_expression.Regex
        The regular expression

    graph : networkx.MultiDiGraph
        The graph representation of the automaton

    start_nodes : set[Hashable], optional
        A finite set of start states - graph nodes

    final_nodes : set[Hashable], optional
        A finite set of final states - graph nodes

    separate_flag : bool, optional
        Flag of chose mode

    Returns
    -------
    result : set[Hashable]
        set[nodes] for not separated mode
        set[(start_node, final_node)] for separated mode

    """
    nfa = build_nfa(graph, start_nodes, final_nodes)
    dfa = build_minimal_dfa(regex)

    nfa_bm = BoolMatrix(nfa)
    dfa_bm = BoolMatrix(dfa)

    result = nfa_bm.bfs(dfa_bm, separate_flag)
    return result
