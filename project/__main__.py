import sys
from pathlib import Path
from project import get_graph_info, create_and_save_two_cycles_graph


def main():
    # example 1
    try:
        bzip_info = get_graph_info("bzip")
        print("bzip info:")
        print(f"nodes:  {bzip_info['nodes']}")
        print(f"edges:  {bzip_info['edges']}")
        print(f"labels: {bzip_info['labels']}")
    except Exception as e:
        print(f"could not retrieve info for bzip: {e}", file=sys.stderr)

    # example 2
    try:
        output_file = Path("two_cycles_graph.dot")
        create_and_save_two_cycles_graph(
            nodes_count1=5,
            nodes_count2=4,
            labels=("a", "b"),
            output_path=str(output_file),
        )
    except Exception as e:
        print(f"could not create two cycles graph: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
