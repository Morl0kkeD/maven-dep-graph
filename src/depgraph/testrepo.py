"""Модуль для чтения тестового графа из файла."""

import re

LINE_RE = re.compile(r"^([A-Z]+):(.*)$")


def load_test_graph(path: str) -> dict[str, list[str]]:
    """Загрузить граф из текстового файла."""
    graph = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = LINE_RE.match(line)
            if not match:
                raise ValueError(f"Некорректная строка: {line}")
            node = match.group(1)
            deps_str = match.group(2).strip()
            deps = [d.strip() for d in deps_str.split(",") if d.strip()]
            graph[node] = deps
    return graph