from dataclasses import dataclass

import cfpq_data


@dataclass
class GraphMetadata:
    node_count: int
    edge_count: int
    edge_labels: set


def get_graph_metadata(graph_name: str) -> GraphMetadata:
    graph = cfpq_data.graph_from_csv(cfpq_data.download(graph_name))
    return GraphMetadata(
        node_count=graph.number_of_nodes(),
        edge_count=graph.number_of_edges(),
        edge_labels={lbl for _, _, lbl in graph.edges(data="label")},
    )
