"""Валидаторы параметров командной строки."""

import re

MODES = ("url", "file")
NAME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9_.-]*$")
VERSION_RE = re.compile(r"^\d+(\.\d+){0,3}([.-][\w]+)?$")


def validate_package_name(value: str) -> str:
    """Проверить имя пакета."""
    if not NAME_RE.match(value):
        raise ValueError(f"Некорректное имя пакета: {value!r}")
    return value


def validate_repo_url(value: str, mode: str) -> str:
    """Проверить URL или путь к файлу в зависимости от режима."""
    if mode == "url":
        if not value.startswith(("http://", "https://")):
            raise ValueError(f"Ожидался URL: {value!r}")
        return value
    if not value:
        raise ValueError("Путь к файлу не может быть пустым")
    return value


def validate_mode(value: str) -> str:
    """Проверить режим работы с тестовым репозиторием."""
    if value not in MODES:
        raise ValueError(f"Режим должен быть одним из {MODES}")
    return value


def validate_version(value: str) -> str:
    """Проверить версию пакета."""
    if not VERSION_RE.match(value):
        raise ValueError(f"Некорректная версия: {value!r}")
    return value


def validate_max_depth(value: str) -> int:
    """Проверить максимальную глубину анализа."""
    try:
        depth = int(value)
    except ValueError as exc:
        raise ValueError(f"Глубина должна быть целым числом: {value!r}") from exc
    if depth < 1:
        raise ValueError("Глубина должна быть >= 1")
    return depth