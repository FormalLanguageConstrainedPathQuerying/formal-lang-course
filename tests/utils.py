import inspect
import json
import pathlib
import pydot

import networkx as nx
import pyformlang.finite_automaton as fa


def get_data(name, configurator) -> list:
    with pathlib.Path(inspect.stack()[1].filename) as f:
        parent = f.parent
    with open(parent / f"{name}.json") as f:
        data = json.load(f)
    return [configurator(block) for block in data[name]]


def dot_to_graph(dot: str) -> nx.MultiDiGraph:
    return nx.drawing.nx_pydot.from_pydot(pydot.graph_from_dot_data(dot)[0])


def dot_to_nfa(dot: str) -> fa.EpsilonNFA:
    graph = dot_to_graph(dot)
    for _, data in graph.nodes.data():
        if data["is_start"] in ("True", "False"):
            data["is_start"] = data["is_start"] == "True"
        if data["is_final"] in ("True", "False"):
            data["is_final"] = data["is_final"] == "True"
    for _, _, data in graph.edges.data():
        if data["label"] == "epsilon":
            data["label"] = fa.Epsilon

    return fa.EpsilonNFA.from_networkx(graph)


def eq_automata(
    fa1: fa.DeterministicFiniteAutomaton,
    fa2: fa.DeterministicFiniteAutomaton,
) -> bool:
    min1 = fa1.minimize()
    min2 = fa2.minimize()
    return (
        len(min1.start_states) == 0
        and len(min2.start_states) == 0
        or fa1.is_equivalent_to(fa2)
    )
