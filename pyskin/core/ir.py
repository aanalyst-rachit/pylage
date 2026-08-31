from __future__ import annotations

import copy
from typing import Any


class IRNode:
    """Minimal compiler-layer intermediate representation node."""

    VALID_NODE_TYPES = {"component"}

    def __init__(
        self,
        node_id: str,
        node_type: str,
        component_id: str | None = None,
        props: dict[str, Any] | None = None,
        children: list["IRNode"] | None = None,
        style_ref: Any = None,
    ) -> None:
        self._validate_node_id(node_id)
        self._validate_node_type(node_type)
        self._validate_component_id(component_id, node_type)
        self._validate_props(props)
        self._validate_children(children)

        self.node_id = node_id
        self.node_type = node_type
        self.component_id = component_id
        self.props = copy.deepcopy(props) if props is not None else {}
        self.children = list(children) if children is not None else []
        self.style_ref = style_ref

    @staticmethod
    def _validate_node_id(node_id: str) -> None:
        if not isinstance(node_id, str) or not node_id:
            raise ValueError("node_id must be a non-empty string")

    @classmethod
    def _validate_node_type(cls, node_type: str) -> None:
        if node_type not in cls.VALID_NODE_TYPES:
            raise ValueError(
                f"Invalid node_type: {node_type!r}. "
                f"Must be one of: {cls.VALID_NODE_TYPES}"
            )

    @staticmethod
    def _validate_component_id(
        component_id: str | None,
        node_type: str,
    ) -> None:
        if node_type == "component":
            if not isinstance(component_id, str) or not component_id:
                raise ValueError(
                    "component_id must be a non-empty string "
                    "for component nodes"
                )

    @staticmethod
    def _validate_props(
        props: dict[str, Any] | None,
    ) -> None:
        if props is not None and not isinstance(props, dict):
            raise ValueError("props must be a dictionary or None")

    @staticmethod
    def _validate_children(
        children: list["IRNode"] | None,
    ) -> None:
        if children is None:
            return

        if not isinstance(children, list):
            raise ValueError("children must be a list or None")

        for child in children:
            if not isinstance(child, IRNode):
                raise ValueError(
                    "All children must be IRNode instances"
                )

    def add_child(self, child: "IRNode") -> None:
        """Append one IR child while preserving insertion order."""

        if not isinstance(child, IRNode):
            raise ValueError("Child must be an IRNode instance")

        self.children.append(child)

    def __repr__(self) -> str:
        return (
            "IRNode("
            f"node_id={self.node_id!r}, "
            f"node_type={self.node_type!r}, "
            f"component_id={self.component_id!r}, "
            f"props={self.props!r}, "
            f"style_ref={self.style_ref!r}, "
            f"children={self.children!r}"
            ")"
        )


def snapshot_to_ir(snapshot: dict[str, Any]) -> IRNode:
    """Convert a PySkin snapshot into compiler-layer IR."""

    if not isinstance(snapshot, dict):
        raise TypeError("snapshot must be a dictionary")

    if "id" not in snapshot:
        raise ValueError("snapshot must contain 'id'")

    if "type" not in snapshot:
        raise ValueError("snapshot must contain 'type'")

    node_id = snapshot["id"]
    component_id = snapshot["type"]

    props = snapshot.get("props", {})
    children = snapshot.get("children", [])

    if not isinstance(children, list):
        raise ValueError("snapshot children must be a list")

    ir_children = [
        snapshot_to_ir(child)
        for child in children
    ]

    return IRNode(
        node_id=node_id,
        node_type="component",
        component_id=component_id,
        props=copy.deepcopy(props),
        children=ir_children,
        style_ref=None,
    )
