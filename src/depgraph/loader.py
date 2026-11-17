"""Модуль для определения порядка загрузки зависимостей."""

from collections import deque


def load_order(graph: dict[str, list[str]]) -> list[str]:
    """Вернуть порядок загрузки узлов (топологическая сортировка Кана)."""
    in_degree = {node: 0 for node in graph}
    for deps in graph.values():
        for dep in deps:
            if dep in in_degree:
                in_degree[dep] += 1

    queue = deque([node for node in graph if in_degree[node] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for dep in graph.get(node, []):
            if dep in in_degree:
                in_degree[dep] -= 1
                if in_degree[dep] == 0:
                    queue.append(dep)

    for node in graph:
        if node not in order:
            order.append(node)

        return order[::-1]
