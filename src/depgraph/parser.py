"""Модуль для парсинга XML-файлов Maven (pom.xml)."""

import xml.etree.ElementTree as ET

POM_NAMESPACE = "{http://maven.apache.org/POM/4.0.0}"


def parse_dependencies(pom_xml: str) -> list[tuple[str, str, str]]:
    """Извлечь прямые зависимости из pom.xml."""
    try:
        root = ET.fromstring(pom_xml)
    except ET.ParseError as exc:
        raise ValueError("Некорректный XML в POM-файле") from exc

    deps = []
    deps_node = root.find(f"{POM_NAMESPACE}dependencies")
    if deps_node is None:
        return deps

    for dep in deps_node.findall(f"{POM_NAMESPACE}dependency"):
        group = dep.findtext(f"{POM_NAMESPACE}groupId", "")
        artifact = dep.findtext(f"{POM_NAMESPACE}artifactId", "")
        version = dep.findtext(f"{POM_NAMESPACE}version", "")
        
        if group and artifact:
            deps.append((group, artifact, version))
            
    return deps