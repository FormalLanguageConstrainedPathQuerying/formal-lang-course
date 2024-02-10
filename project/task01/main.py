from pathlib import Path
import cfpq_data as cfpq

from networkx import MultiDiGraph
from networkx.classes.reportviews import OutMultiEdgeView
from networkx.drawing.nx_pydot import write_dot

from dataclasses import dataclass


@dataclass
class GraphProps:
    nodes_count: int
    edges_count: int
    edges_data: OutMultiEdgeView


def get_graph_props_by_name(name: str) -> GraphProps:
    graph_path: Path = cfpq.download(name=name)
    graph: MultiDiGraph = cfpq.graph_from_csv(path=graph_path)
    return GraphProps(
            nodes_count=graph.number_of_nodes(),
            edges_count=graph.number_of_edges(),
            edges_data=graph.edges(data=True)
    )


def two_cycle_graph_to_dot(
        path: str, n: int, m: int,
        *, labels: tuple[str, str] = ("a", "b")):
    graph: MultiDiGraph = \
            cfpq.labeled_two_cycles_graph(n=n, m=m, labels=labels)
    write_dot(G=graph, path=path)
