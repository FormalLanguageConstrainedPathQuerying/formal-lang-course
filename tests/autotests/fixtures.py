import pytest
from helper import generate_rnd_graph
from networkx import MultiDiGraph
from constants import LABELS


@pytest.fixture(scope="function", params=range(5))
def graph(request) -> MultiDiGraph:
    return generate_rnd_graph(20, 40, LABELS)


@pytest.fixture(scope="function", params=range(8))
def small_graph(request) -> MultiDiGraph:
    return generate_rnd_graph(1, 20, LABELS)
