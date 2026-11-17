"""Тесты CLI-парсера."""

import pytest

from depgraph.cli import parse_config


def test_valid_config() -> None:
    """Корректные параметры проходят валидацию."""
    cfg = parse_config([
        "--package", "com.example.app",
        "--repo", "https://repo1.maven.org/maven2",
        "--mode", "url",
        "--version", "1.0.0",
        "--depth", "5",
        "--filter", "test",
    ])
    assert cfg.package_name == "com.example.app"
    assert cfg.max_depth == 5
    assert cfg.filter_substring == "test"


def test_bad_package_name() -> None:
    """Имя, начинающееся с цифры, отвергается."""
    with pytest.raises(ValueError):
        parse_config([
            "--package", "1bad",
            "--repo", "https://x",
            "--version", "1.0",
        ])


def test_bad_url_mode() -> None:
    """В режиме url путь к файлу не принимается."""
    with pytest.raises(ValueError):
        parse_config([
            "--package", "a",
            "--repo", "/tmp/x",
            "--mode", "url",
            "--version", "1.0",
        ])


def test_bad_depth() -> None:
    """Отрицательная глубина отвергается."""
    with pytest.raises(ValueError):
        parse_config([
            "--package", "a",
            "--repo", "https://x",
            "--version", "1.0",
            "--depth", "-1",
        ])