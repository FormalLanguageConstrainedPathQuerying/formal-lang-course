import time
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

import cfpq_data
from tabulate import tabulate
from pyformlang.regular_expression import Regex
from scipy.sparse import lil_matrix, csr_matrix, csc_matrix
from scipy import mean
from scipy.stats import tstd

from project.t2_finite_automata import (
    build_minimal_dfa_from_regex,
    build_nfa_from_graph,
)
from project.t3_boolean_matrix_automata import *
import project.t1_graph_module as gm


# def test_rpq_with_separated():
#     def regex_for_graph(gr):
#         ls = list()
#         for edge in gr.edges(data="label"):
#             ls.append(edge[2])
#         ls = [label for (label, _) in Counter(ls).most_common(4)]
#         return [
#             Regex(f"({ls[1]}|{ls[2]}|{ls[3]})*{ls[0]}"),
#             Regex(f"({ls[0]}|{ls[1]}|{ls[2]})({ls[0]}|{ls[1]}|{ls[2]})*{ls[3]}"),
#             Regex(f"({ls[0]} {ls[1]})* ({ls[0]} {ls[2]})*"),
#             Regex(f"{ls[0]} {ls[2]} ({ls[0]}|{ls[3]})*"),
#         ]
#
#     # def regex_from_list(ls) -> Regex:
#     #     return Regex(f"({'|'.join(ls)})*")
#
#     print()
#     matrix_types = [lil_matrix, csr_matrix, csc_matrix, dok_matrix]
#     graphs = ["skos", "generations"]
#     # graphs = ['ls', 'core']travel
#     # regex = Regex("type*")
#     # table = list()
#     for graph_name in graphs:
#         graph = gm.get_graph_by_name(graph_name)
#         bool_matrix_for_graph = BooleanMatrixAutomata(
#             build_nfa_from_graph(graph, None, None), matrix_types[0]
#         )
#         regexes = regex_for_graph(graph)
#         t = {mat: {mean: [], tstd: []} for mat in matrix_types}
#         for nr, regex in enumerate(regexes):
#             bool_matrix_for_regex = BooleanMatrixAutomata(
#                 build_minimal_dfa_from_regex(regex), matrix_types[0]
#             )
#             for nmt, mat_type in enumerate(matrix_types):
#                 times = list()
#                 for i in range(5):
#                     bool_matrix_for_graph.type_of_matrix = mat_type
#                     bool_matrix_for_regex.type_of_matrix = mat_type
#                     start_time = time.time()
#                     bool_matrix_for_graph.bfs_based_rpq(bool_matrix_for_regex, False)
#                     times.append(time.time() - start_time)
#                 mean_t = mean(times)
#                 tstd_t = tstd(times)
#                 # table.append([graph_name, nr, mat_type.__name__, f'{mean_t:.7f}', f'{tstd_t:.7f}'])
#                 t[mat_type][mean].append(mean_t)
#                 t[mat_type][tstd].append(tstd_t)
#
#         index = np.arange(0, 5, 1.25)
#         bw = 0.28
#         # plt.axis([0, 5, 0, 0.04])
#         colors = ["r", "g", "b", "y"]
#         for i, mat in enumerate(matrix_types):
#             plt.bar(
#                 index + i * bw,
#                 t[mat][mean],
#                 bw,
#                 yerr=t[mat][tstd],
#                 error_kw={"ecolor": "0.1", "capsize": 6},
#                 alpha=0.7,
#                 color=colors[i],
#                 label=mat.__name__,
#             )
#         plt.xticks(index + 2 * bw, ["A", "B", "C", "D"])
#         plt.title(graph_name)
#         plt.legend(loc=1)
#         plt.show()
#     # print(tabulate(table, ['Graph name', 'regex', 'matrix', 'average time', 'deviation'], "simple_outline"))


def test_rpq_without_separated():
    graph = cfpq_data.labeled_two_cycles_graph(3, 3, labels=("a", "b"))
    regex = Regex("(a*|b)")
    bool_matrix_for_graph = BooleanMatrixAutomata(
        build_nfa_from_graph(graph, None, None)
    )
    bool_matrix_for_regex = BooleanMatrixAutomata(build_minimal_dfa_from_regex(regex))
    result = bool_matrix_for_graph.bfs_based_rpq(bool_matrix_for_regex, False)

    expected_result = {0, 1, 2, 3, 4, 5, 6}

    assert result == expected_result
