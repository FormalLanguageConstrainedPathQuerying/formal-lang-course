import argparse
import sys
from project.graph_utils import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-get_graph_description",
        metavar="NAME",
        type=str,
        help="Returns number of nodes, number of edges, set of labels",
    )

    group.add_argument(
        "-write_two_cycles_graph",
        nargs=5,
        metavar=(
            "FIRST_SIZE",
            "SECOND_SIZE",
            "FIRST_LABEL",
            "SECOND_LABEL",
            "OUTPUT_FILE",
        ),
        action="store",
        help="Creates and writes a graph of two loops along a given path",
    )

    args = parser.parse_args()
    if args.get_graph_description is not None:

        name = args.get_graph_description
        if all(
            name not in cfpq_data.DATASET[graph_class].keys()
            for graph_class in cfpq_data.DATASET.keys()
        ):
            print("No graph with such name", file=sys.stderr)
            exit(1)
        graph = cfpq_data.graph_from_dataset(name, verbose=False)
        print(get_graph_description(graph))

    else:

        write_two_cycles_graph_args = args.write_two_cycles_graph
        if not (
            write_two_cycles_graph_args[0].isdigit()
            and write_two_cycles_graph_args[1].isdigit()
        ):
            print("Size of cycles should be integer", file=sys.stderr)
            exit(1)
        write_two_cycles_graph(
            int(write_two_cycles_graph_args[0]),
            int(write_two_cycles_graph_args[1]),
            (write_two_cycles_graph_args[2], write_two_cycles_graph_args[3]),
            write_two_cycles_graph_args[4],
        )
