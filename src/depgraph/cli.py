"""Парсинг аргументов командной строки и вывод конфигурации."""

import argparse
import sys

from .config import Config
from . import validators
from .fetcher import build_pom_url, fetch_pom
from .parser import parse_dependencies
from .testrepo import load_test_graph
from .graph import build_graph
from .loader import load_order
from .visualizer import to_plantuml, render_plantuml


def build_parser() -> argparse.ArgumentParser:
    """Собрать парсер аргументов."""
    parser = argparse.ArgumentParser(
        prog="depgraph",
        description="Построение графа зависимостей Maven-пакетов",
    )
    parser.add_argument(
        "--package",
        required=True,
        help="Имя пакета (group:artifact)"
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="URL или путь к файлу"
    )
    parser.add_argument(
        "--mode",
        choices=validators.MODES,
        default="url",
        help="Режим работы с тестовым репозиторием",
    )
    parser.add_argument("--version", required=True, help="Версия пакета")
    parser.add_argument(
        "--depth", type=int, default=3, help="Глубина анализа"
    )
    parser.add_argument(
        "--filter",
        default="",
        help="Подстрока для фильтрации пакетов"
    )
    parser.add_argument(
        "--direct",
        action="store_true",
        help="Показать только прямые зависимости"
    )
    parser.add_argument(
        "--show-graph",
        action="store_true",
        help="Построить и вывести граф"
    )
    parser.add_argument(
        "--show-load-order",
        action="store_true",
        help="Показать порядок загрузки"
    )
    parser.add_argument("--render", help="Путь для сохранения PNG-картинки")
    return parser


def parse_config(argv: list[str]) -> Config:
    """Разобрать argv и провалидировать параметры."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return Config(
        package_name=validators.validate_package_name(args.package),
        repo_url=validators.validate_repo_url(args.repo, args.mode),
        repo_mode=validators.validate_mode(args.mode),
        package_version=validators.validate_version(args.version),
        max_depth=validators.validate_max_depth(str(args.depth)),
        filter_substring=args.filter,
        direct=args.direct,
        show_graph=args.show_graph,
        show_load_order=args.show_load_order,
        render=args.render,
    )


def print_config(config: Config) -> None:
    """Вывести конфигурацию в формате ключ-значение."""
    items = [
        ("package_name", config.package_name),
        ("repo_url", config.repo_url),
        ("repo_mode", config.repo_mode),
        ("package_version", config.package_version),
        ("max_depth", config.max_depth),
        ("filter_substring", config.filter_substring or "<none>"),
    ]
    for key, value in items:
        print(f"{key} = {value}")


def get_fetch_fn(config: Config):
    """Создать функцию для получения прямых зависимостей."""
    if config.repo_mode == "file":
        data = load_test_graph(config.repo_url)
        return lambda node: data.get(node, [])

    def fetch(node: str) -> list[str]:
        if ":" not in node:
            return []
        group, artifact = node.split(":")
        url = build_pom_url(
            config.repo_url, group, artifact, config.package_version
        )
        try:
            xml = fetch_pom(url)
            deps = parse_dependencies(xml)
            return [f"{g}:{a}" for g, a, v in deps]
        except ValueError:
            return []
    return fetch


def main(argv: list[str] | None = None) -> int:
    """Точка входа CLI."""
    try:
        config = parse_config(argv if argv is not None else sys.argv[1:])
    except ValueError as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 2

    if config.direct:
        if config.repo_mode != "url":
            print("Флаг --direct только для 'url'", file=sys.stderr)
            return 1
        try:
            group, artifact = config.package_name.split(":")
        except ValueError:
            print("Формат пакета: groupId:artifactId", file=sys.stderr)
            return 1
        url = build_pom_url(
            config.repo_url, group, artifact, config.package_version
        )
        print(f"Скачивание: {url}")
        try:
            xml = fetch_pom(url)
            deps = parse_dependencies(xml)
        except ValueError as exc:
            print(f"Ошибка: {exc}", file=sys.stderr)
            return 1
        print(f"Прямые зависимости для {config.package_name}:")
        print(f"  Версия: {config.package_version}")
        if not deps:
            print("  (нет)")
        for d in deps:
            print(f"  {d[0]}:{d[1]}:{d[2] if d[2] else 'auto'}")
        return 0

    if config.show_graph:
        fetch_fn = get_fetch_fn(config)
        graph = build_graph(
            config.package_name,
            config.max_depth,
            config.filter_substring,
            fetch_fn
        )
        print("Граф зависимостей:")
        for node, deps in graph.items():
            deps_str = ", ".join(deps) if deps else "(нет)"
            print(f"  {node} -> {deps_str}")
        return 0

    if config.show_load_order:
        fetch_fn = get_fetch_fn(config)
        graph = build_graph(
            config.package_name,
            config.max_depth,
            config.filter_substring,
            fetch_fn
        )
        order = load_order(graph)
        print("Порядок загрузки:")
        for i, node in enumerate(order, 1):
            print(f"  {i}. {node}")
        return 0

    if config.render:
        fetch_fn = get_fetch_fn(config)
        graph = build_graph(
            config.package_name,
            config.max_depth,
            config.filter_substring,
            fetch_fn
        )
        uml = to_plantuml(graph)
        try:
            png_path = render_plantuml(uml, config.render)
            print(f"Картинка сохранена: {png_path}")
        except FileNotFoundError as exc:
            print(f"Ошибка: {exc}", file=sys.stderr)
            return 1
        return 0

    print_config(config)
    return 0
