import inspect
import json
import pathlib

import networkx as nx
import pydot


def read_data_from_json(name, configurator):
    with pathlib.Path(inspect.stack()[1].filename) as f:
        parent = f.parent
    with open(parent / f"{name}.json") as f:
        data = json.load(f)
    return [configurator(block) for block in data[name]]


def dot_to_graph(dot: str) -> nx.MultiDiGraph:
    return nx.drawing.nx_pydot.from_pydot(pydot.graph_from_dot_data(dot)[0])
