import networkx as nx
import pytest
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from scipy.sparse import dok_matrix

from project.boolean_decompositon import BooleanDecomposition, decomposition_to_automaton
from project.regex_utils import create_nfa_from_graph
from tests.test_task3.utils import dot_to_graph, get_data


@pytest.mark.parametrize(
    "actual, expected",
    get_data(
        "test_closure",
        lambda data: (
                BooleanDecomposition(create_nfa_from_graph(
                    dot_to_graph(data["graph"]),
                    start_states=data["starts"],
                    final_states=data["finals"])
                ),
                data["matrix"]
        ),
    ),
)
def test_transitive_closure(actual: BooleanDecomposition, expected):
    if len(expected) == 0:
        assert actual.make_transitive_closure().size == 0
    else:
        assert actual.make_transitive_closure().toarray().data.__eq__(dok_matrix(expected).toarray().data)


@pytest.mark.parametrize(
    "expected",
    get_data(
        "test_to_automaton",
        lambda data: (
                create_nfa_from_graph(dot_to_graph(data["expected"]))
        )
    ),
)
def test_to_automaton(expected: NondeterministicFiniteAutomaton):
    actual = decomposition_to_automaton(BooleanDecomposition(expected))
    assert nx.drawing.nx_pydot.to_pydot(actual.to_networkx()).__str__() == nx.drawing.nx_pydot.to_pydot(expected.to_networkx()).__str__()


@pytest.mark.parametrize(
    "decomposition, expected, starts, finals",
    get_data(
        "test_init",
        lambda data: (
            BooleanDecomposition(create_nfa_from_graph(
                dot_to_graph(data["decomposition"]),
                start_states=data["starts"],
                final_states=data["finals"]
            )),
            data["expected"],
            set(data["starts"]),
            set(data["finals"])
        )
    ),
)
def test_init(decomposition: BooleanDecomposition, expected, starts, finals):
    def eq_matrix(arr1, arr2):
        acc = True
        for i in range(len(arr1)):
            for j in range(len(arr1[i])):
                acc = acc and (arr1[i][j] == arr2[i][j])

        return acc

    isMatriciesCorrect = True
    for (letter, values) in decomposition.bool_decomposition.items():
        isMatriciesCorrect = isMatriciesCorrect and eq_matrix(expected[letter], values.toarray())

    assert isMatriciesCorrect \
           and decomposition.get_start_states() == starts \
           and decomposition.get_final_states() == finals
