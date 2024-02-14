import pydot
import cfpq_data


def get_graph_info(graph_name):
    """
    Возвращает информацию о графе: количество вершин, рёбер и перечисляет различные метки на рёбрах.
    """
    graph = cfpq_data.graph_from_dataset(graph_name)
    num_vertices = len(graph.nodes)
    num_edges = len(graph.edges)
    edge_labels = set()
    for _, _, data in graph.edges(data=True):
        if 'label' in data:
            edge_labels.add(data['label'])
    return num_vertices, num_edges, list(edge_labels)


def build_and_save_graph(num_vertices, labels, output_file):
    graph = pydot.Dot(graph_type='graph')

    # Создаем вершины и добавляем в граф
    for i in range(num_vertices):
        node = pydot.Node(str(i))
        graph.add_node(node)

    # Создаем рёбра для первого цикла
    for i in range(num_vertices):
        src = str(i)
        dst = str((i + 1) % num_vertices)
        edge = pydot.Edge(src, dst, label=labels[0])
        graph.add_edge(edge)

    # Создаем рёбра для второго цикла
    for i in range(num_vertices):
        src = str(i)
        dst = str((i + 1) % num_vertices + num_vertices)
        edge = pydot.Edge(src, dst, label=labels[1])
        graph.add_edge(edge)

    # Создаем рёбра между циклами
    for i in range(num_vertices):
        src = str(i)
        dst = str((i + 1) % num_vertices + num_vertices)
        edge = pydot.Edge(src, dst, label=labels[2])
        graph.add_edge(edge)

    # Сохраняем граф в файл
    graph.write(output_file, format='dot')
