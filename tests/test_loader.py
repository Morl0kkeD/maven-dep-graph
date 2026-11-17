"""Тесты порядка загрузки."""

from pathlib import Path

from depgraph.graph import build_graph
from depgraph.testrepo import load_test_graph
from depgraph.loader import load_order

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def get_fetch_fn(filename: str):
    """Загрузить тестовый граф."""
    path = FIXTURES_DIR / filename
    data = load_test_graph(str(path))
    def fetch(node: str) -> list[str]:
        return data.get(node, [])
    return fetch


def test_load_order_chain() -> None:
    """Для цепочки A->B->C->D порядок должен быть D, C, B, A."""
    fetch = get_fetch_fn("chain.txt")
    graph = build_graph("A", 10, "", fetch)
    order = load_order(graph)
    assert order == ["D", "C", "B", "A"]


def test_load_order_diamond() -> None:
    """Для ромба D должен быть загружен раньше B и C."""
    fetch = get_fetch_fn("diamond.txt")
    graph = build_graph("A", 10, "", fetch)
    order = load_order(graph)
    assert order[0] == "D"
    assert order[-1] == "A"