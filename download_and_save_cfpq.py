import sys
from project import save_graph_as_dot, get_graph_info_by_name

n = len(sys.argv)
if n != 3:
    raise Exception(f"invalid count of argument, 2 arguments expected, {n - 1} given")

print(f"download graph {sys.argv[1]}")
print(f"save it to {sys.argv[2]}")


save_graph_as_dot(get_graph_info_by_name(sys.argv[1]).graph, sys.argv[2])
