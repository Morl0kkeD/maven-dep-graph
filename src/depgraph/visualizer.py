"""Модуль для визуализации графа зависимостей через PlantUML."""

import subprocess
from pathlib import Path


def to_plantuml(graph: dict[str, list[str]]) -> str:
    """Сгенерировать текст PlantUML для графа зависимостей."""
    lines = ["@startuml", "skinparam linetype ortho"]

    # Объявляем узлы
    for node in graph:
        safe_node = node.replace(":", "_").replace(".", "_")
        lines.append(f'node "{node}" as {safe_node}')

    # Рисуем стрелки
    for node, deps in graph.items():
        src = node.replace(":", "_").replace(".", "_")
        for dep in deps:
            dst = dep.replace(":", "_").replace(".", "_")
            lines.append(f"{src} --> {dst}")

    lines.append("@enduml")
    return "\n".join(lines)


def render_plantuml(uml_text: str, output_path: str) -> str:
    """Сохранить текст PlantUML в файл и отрендерить его в PNG."""
    puml_file = Path(output_path).with_suffix(".puml")
    puml_file.write_text(uml_text, encoding="utf-8")

    jar_path = Path("plantuml.jar").resolve()
    if not jar_path.exists():
        raise FileNotFoundError("plantuml.jar не найден в корне проекта")

    subprocess.run(
        ["java", "-jar", str(jar_path), str(puml_file)],
        check=True,
        capture_output=True
    )
    return str(Path(output_path).with_suffix(".png"))
