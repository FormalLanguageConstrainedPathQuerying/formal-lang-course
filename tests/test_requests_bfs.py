from project.requests_bfs import *
from pyformlang.regular_expression import Regex
import cfpq_data as cfpq
import random


def random_regex():
    base = ["a b c", "a (b | c)", "a (b | c)*", "a (b | c)*c", "a b* c", "a* b* c*", "(a b c)*", "(a (b c)*)*"]
    return base[random.randint(0, len(base) - 1)]


def create_two_cycles_graph(nns, ls):
    return cfpq.labeled_two_cycles_graph(nns[0], nns[1], labels=ls)


def test_reachable_vertices():
    regex = "(0|1)*"
    graph = create_two_cycles_graph((1, 2), ["0", "1"])

    assert {0, 1, 2, 3} == reachable_vertices(regex_to_dka(Regex(regex)), graph, [1, 2, 3])
    assert {0, 1, 2, 3} == reachable_vertices(regex_to_dka(Regex(regex)), graph, [1, 3, 3])
    assert {0, 1, 2, 3} == reachable_vertices(regex_to_dka(Regex(regex)), graph, [1, 2])
    assert {0, 1, 2, 3} == reachable_vertices(regex_to_dka(Regex(regex)), graph, [0])

    assert {0: {0, 1, 2, 3}} == reachable_vertices(regex_to_dka(Regex(regex)), graph, [0], True)
    assert {0, 1, 2, 3} == reachable_vertices(regex_to_dka(Regex(regex)), graph, [0], False)
    assert {1: {0, 1, 2, 3}, 2: {0, 1, 2, 3}, 3: {0, 1, 2, 3}} == reachable_vertices(regex_to_dka(Regex(regex)), graph,
                                                                                     [1, 2, 3], True)
    assert {0, 1, 2, 3} == reachable_vertices(regex_to_dka(Regex(regex)), graph, [1, 2, 3], False)


def test_bfs_graph_regular_query():
    regex = "(0|1)*"
    graph = create_two_cycles_graph((1, 2), ["0", "1"])

    assert {0} == bfs_graph_request(graph, [0], [0], regex)
    assert {1} == bfs_graph_request(graph, [0], [1], regex)
    assert {0} == bfs_graph_request(graph, [1], [0], regex)
    assert {1, 2} == bfs_graph_request(graph, [0, 1], [1, 2], regex)

    assert {0: {0}} == bfs_graph_request(graph, [0], [0], regex, True)
    assert {0} == bfs_graph_request(graph, [0], [0], regex, False)
    assert {0: {1}} == bfs_graph_request(graph, [0], [1], regex, True)
    assert {1} == bfs_graph_request(graph, [0], [1], regex, False)
    assert {0: {1, 2}, 1: {1, 2}} == bfs_graph_request(graph, [0, 1], [1, 2], regex, True)
    assert {1, 2} == bfs_graph_request(graph, [0, 1], [1, 2], regex, False)
