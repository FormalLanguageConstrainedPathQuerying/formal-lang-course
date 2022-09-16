import networkx as nx


def find_cycles(graph: nx.MultiDiGraph) -> list:
    todo = set(graph.nodes)
    cycles = []

    def ret(path, queue):
        if not queue:
            return (path, queue, (False, 0))
        key = queue.pop()
        while key[0] == -1:
            path.pop()
            if not queue:
                return (path, queue, (False, 0))
            key = queue.pop()
        return (path, queue, (True, key[1]))

    while todo:
        curr = todo.pop()
        start = curr
        todo.add(curr)

        path = []
        queue = []
        visited = set()
        while True:
            flag = True
            while not (curr in todo):
                path, queue, (flag, curr) = ret(path, queue)
                if not flag:
                    break
            if not flag:
                break
            if curr in visited:
                if curr == start:
                    cycles.append(list(path))
                path, queue, (flag, curr) = ret(path, queue)
                if not flag:
                    break
                continue
            path.append(curr)
            visited.add(curr)
            queue += [(-1, 0)] + [(0, i) for i in list(graph[curr])]
            path, queue, (flag, curr) = ret(path, queue)
            if not flag:
                break
        todo.remove(start)
    return cycles
