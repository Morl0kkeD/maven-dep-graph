"""Тесты парсера pom.xml."""

import pytest
from depgraph.parser import parse_dependencies


def test_parse_valid_pom() -> None:
    """Тест извлечения двух зависимостей."""
    xml = """<project xmlns="http://maven.apache.org/POM/4.0.0">
      <dependencies>
        <dependency>
          <groupId>org.slf4j</groupId>
          <artifactId>slf4j-api</artifactId>
          <version>2.0.9</version>
        </dependency>
        <dependency>
          <groupId>com.google.guava</groupId>
          <artifactId>guava</artifactId>
          <version>32.1.3-jre</version>
        </dependency>
      </dependencies>
    </project>"""
    
    deps = parse_dependencies(xml)
    assert len(deps) == 2
    assert deps[0] == ("org.slf4j", "slf4j-api", "2.0.9")
    assert deps[1] == ("com.google.guava", "guava", "32.1.3-jre")


def test_parse_no_deps() -> None:
    """Тест POM без зависимостей."""
    xml = '<project xmlns="http://maven.apache.org/POM/4.0.0"></project>'
    assert parse_dependencies(xml) == []


def test_parse_invalid_xml() -> None:
    """Тест битого XML."""
    with pytest.raises(ValueError):
        parse_dependencies("<project><dependencies>")