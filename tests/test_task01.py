import os
import project.task01 as task


def test_props_by_name():
    properties = task.get_graph_properties("bzip")
    allLabels = set()

    for e in properties.edges:
        allLabels.add(e[2]["label"])
    assert properties.nodes_count == 632
    assert properties.edges_count == 556
    assert allLabels == {"a", "d"}
    print(properties.edges_count)
