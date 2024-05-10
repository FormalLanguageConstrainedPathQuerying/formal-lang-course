import pytest
from helper import generate_rnd_graph, generate_rnd_dense_graph
from networkx import MultiDiGraph
from constants import LABELS
import random

funcs = [generate_rnd_dense_graph, generate_rnd_graph]


@pytest.fixture(scope="function", params=range(8))
def graph(request) -> MultiDiGraph:
    fun = random.choice(funcs)
    # task 6 takes a long time if there are ranges [1, 100]
    return fun(1, 40, LABELS)
