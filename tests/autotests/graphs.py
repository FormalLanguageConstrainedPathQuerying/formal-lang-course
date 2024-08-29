from networkx import MultiDiGraph
from constants import LABEL

point_graph = MultiDiGraph()
point_graph.add_node(1)

set_of_vertices_without_edges = MultiDiGraph()
set_of_vertices_without_edges.add_nodes_from([0, 1, 2])

b_graph = MultiDiGraph()
b_graph.add_edges_from([(0, 1, {LABEL: 'b'})])

bbb_graph = MultiDiGraph()
bbb_graph.add_edges_from([
    (0, 1, {LABEL: 'b'}),
    (1, 2, {LABEL: 'b'}),
    (2, 0, {LABEL: 'b'})
])

bab_graph = MultiDiGraph()
bab_graph.add_edges_from([
    (0, 1, {LABEL: 'b'}),
    (1, 2, {LABEL: 'a'}),
    (2, 0, {LABEL: 'b'})
]
)

baa_graph = MultiDiGraph()
baa_graph.add_edges_from([
    (0, 0, {LABEL: 'b'}),
    (0, 1, {LABEL: 'a'}),
    (1, 0, {LABEL: 'a'})
]
)

aaa_graph = MultiDiGraph()
aaa_graph.add_edges_from([
    (0, 1, {LABEL: 'a'}),
    (1, 2, {LABEL: 'a'}),
    (2, 0, {LABEL: 'a'})
])