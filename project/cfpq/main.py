from project.cfpq.graph_worker import GraphWorker
from project.cfpq.utils import create_labeled_two_cycles_graph


def load_graph_info_by_name(name: str) -> dict:
    gw = GraphWorker()
    gw.load_graph_by_name(name)
    return gw.get_graph_info()


def create_and_save_two_cycles_graph(
    first_cycle: tuple[int, str], second_cycle: tuple[int, str], path: str
) -> bool:
    gw = GraphWorker()
    gw.update_graph(
        create_labeled_two_cycles_graph(
            first_cycle[0], first_cycle[1], second_cycle[0], second_cycle[1]
        )
    )
    return gw.save_as_dot_file(path=path)


if __name__ == "__main__":
    print(load_graph_info_by_name("travel"))
    create_and_save_two_cycles_graph((5, "aaa"), (5, "ccc"), "test.dot")
