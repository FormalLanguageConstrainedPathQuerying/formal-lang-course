from project.cfpq.graph_info import GraphInfo


def load_graph_info_by_name(name: str) -> GraphInfo:
    from project.cfpq.io import load_graph_by_name
    from project.cfpq.utils import get_graph_info

    return get_graph_info(load_graph_by_name(name))


def create_and_save_labeled_two_cycles_graph_as_dot_file(
    first_cycle: (int, str),
    second_cycle: (int, str),
    path: str,
):
    from project.cfpq.utils import create_labeled_two_cycles_graph
    from project.cfpq.io import save_graph_as_dot_file

    graph = create_labeled_two_cycles_graph(first_cycle, second_cycle)
    return save_graph_as_dot_file(graph, path)
