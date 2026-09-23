"""Generic Chart backend contract (backend-agnostic)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ChartPayload:
    """JSON-safe, transport-ready chart payload.

    This is the only shape that crosses the ENGINE → client boundary.
    Backends must never leak their native objects into the protocol.
    """

    backend: str
    data: list[dict[str, Any]]
    layout: dict[str, Any]
    config: dict[str, Any] = field(default_factory=dict)
    frames: list[dict[str, Any]] | None = None

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "backend": self.backend,
            "data": self.data,
            "layout": self.layout,
            "config": self.config,
        }
        if self.frames is not None:
            payload["frames"] = self.frames
        return payload


class ChartBackend(ABC):
    """Abstract backend adapter.

    Implementations convert a native figure object into a ChartPayload
    and declare supported interaction capabilities.
    """

    name: str = "base"

    @abstractmethod
    def accept(self, figure: Any) -> bool:
        """Return True if this backend can handle the given figure."""

    @abstractmethod
    def to_payload(
        self,
        figure: Any,
        *,
        config: dict[str, Any] | None = None,
    ) -> ChartPayload:
        """Convert a native figure into a serializable ChartPayload."""

    def capabilities(self) -> dict[str, bool]:
        """Declare supported interaction features."""
        return {
            "click": False,
            "hover": False,
            "select": False,
            "relayout": False,
            "zoom": False,
        }
