"""Тесты построения графа BFS."""

from pathlib import Path

from depgraph.graph import build_graph
from depgraph.testrepo import load_test_graph

# Вычисляем абсолютный путь к папке fixtures
FIXTURES_DIR = Path(__file__).parent / "fixtures"


def get_fetch_fn(filename: str):
    """Вспомогательная функция для загрузки графа и создания fetch_fn."""
    path = FIXTURES_DIR / filename
    data = load_test_graph(str(path))

    def fetch(node: str) -> list[str]:
        return data.get(node, [])
    return fetch


def test_chain_depth() -> None:
    """Цепочка A->B->C->D. При глубине 2 дальше C не идем."""
    fetch = get_fetch_fn("chain.txt")
    graph = build_graph("A", 2, "", fetch)
    assert "A" in graph
    assert "B" in graph
    assert "C" in graph
    assert "D" not in graph


def test_cycle() -> None:
    """Цикл A->B->C->A не должен вызывать зависание."""
    fetch = get_fetch_fn("cycle.txt")
    graph = build_graph("A", 10, "", fetch)
    assert len(graph) == 3
    assert "A" in graph["C"]


def test_diamond() -> None:
    """Ромб: D не должен дублироваться в графе."""
    fetch = get_fetch_fn("diamond.txt")
    graph = build_graph("A", 10, "", fetch)
    assert graph["A"] == ["B", "C"]
    assert graph["B"] == ["D"]
    assert graph["C"] == ["D"]


def test_filter() -> None:
    """Фильтрация: пакеты с 'TEST' исключаются."""
    fetch = get_fetch_fn("filter.txt")
    graph = build_graph("A", 10, "TEST", fetch)
    assert graph["A"] == ["B"]
    assert "TESTX" not in graph
    assert "C" in graph
