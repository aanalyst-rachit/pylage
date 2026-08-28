from __future__ import annotations

from typing import Any

from .component import Component


def print_tree(node: Any, depth: int = 0) -> None:
    indent = "  " * depth

    if isinstance(node, Component):
        print(f"{indent}{node.type} [{node.id}]")

        if node.props:
            print(f"{indent}  props={node.props}")

        for child in node.children:
            print_tree(child, depth + 1)

    else:
        print(f"{indent}{node!r}")


def collect_ids(node: Any) -> list[str]:
    if not isinstance(node, Component):
        return []

    ids = [node.id]

    for child in node.children:
        ids.extend(collect_ids(child))

    return ids


def count_components(node: Any) -> int:
    if not isinstance(node, Component):
        return 0

    return 1 + sum(
        count_components(child)
        for child in node.children
    )
