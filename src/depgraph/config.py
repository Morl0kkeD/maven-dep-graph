"""Конфигурация приложения: параметры командной строки."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    """Настраиваемые пользователем параметры."""

    package_name: str
    repo_url: str
    repo_mode: str
    package_version: str
    max_depth: int
    filter_substring: str
    direct: bool = False
    show_graph: bool = False
    show_load_order: bool = False
    render: str = ""
