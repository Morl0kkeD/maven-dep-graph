"""Модуль для загрузки POM-файлов из репозитория Maven."""

import urllib.request
from urllib.error import HTTPError


def build_pom_url(
    repo_url: str, group_id: str, artifact_id: str, version: str
) -> str:
    """Собрать URL до pom.xml файла по координатам Maven."""
    group_path = group_id.replace(".", "/")
    filename = f"{artifact_id}-{version}.pom"
    repo = repo_url.rstrip("/")
    return f"{repo}/{group_path}/{artifact_id}/{version}/{filename}"


def fetch_pom(url: str) -> str:
    """Скачать pom.xml по URL и вернуть его как строку."""
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode("utf-8")
    except HTTPError as exc:
        raise ValueError(f"Не удалось скачать POM: {url}") from exc
    except urllib.error.URLError as exc:
        raise ValueError(f"Ошибка сети при запросе: {url}") from exc