import sys
from cfpq_data import generate_multiple_source
from project import load_graph_from_dot

n = len(sys.argv)
if n != 4:
    raise Exception(f"invalid count of argument, 3 arguments expected, {n - 1} given")

graph = load_graph_from_dot(sys.argv[1])
source = generate_multiple_source(graph, int(sys.argv[2]))

f = open(sys.argv[3], "w")
for i in source:
    f.print(i)
f.close()
