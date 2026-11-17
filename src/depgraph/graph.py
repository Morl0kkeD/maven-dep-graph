"""Модуль для построения графа зависимостей (BFS)."""

from collections import deque
from typing import Callable


def build_graph(
    root: str,
    depth_limit: int,
    filter_sub: str,
    fetch_fn: Callable[[str], list[str]],
) -> dict[str, list[str]]:
    """Построить граф зависимостей с помощью BFS без рекурсии."""
    graph = {}
    queue = deque([(root, 0)])
    visited = set()

    while queue:
        node, depth = queue.popleft()

        # Пропускаем, если уже видели этот узел
        if node in visited:
            continue
        visited.add(node)

        # Если достигли максимальной глубины, не идем дальше
        if depth >= depth_limit:
            graph[node] = []
            continue

        # Получаем прямые зависимости
        deps = fetch_fn(node)

        # Фильтрация по подстроке (работает только если фильтр задан)
        if filter_sub:
            filtered_deps = [d for d in deps if filter_sub not in d]
        else:
            filtered_deps = deps

        graph[node] = filtered_deps

        for dep in filtered_deps:
            if dep not in visited:
                queue.append((dep, depth + 1))

    return graph