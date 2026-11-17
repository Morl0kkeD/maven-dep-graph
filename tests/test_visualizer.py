"""Тесты визуализатора."""

from depgraph.visualizer import to_plantuml


def test_to_plantuml() -> None:
    """Тест генерации PlantUML-кода."""
    graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
    uml = to_plantuml(graph)
    assert "@startuml" in uml
    assert "@enduml" in uml
    assert "A --> B" in uml
    assert "A --> C" in uml
    assert "B --> D" in uml
