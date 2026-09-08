from __future__ import annotations

from typing import Callable
import threading

from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.dirty import DirtyNodes


class Scheduler:
    """Batches dirty component updates."""

    def __init__(
        self,
        dirty: DirtyNodes,
        callback: Callable[[Component], None],
        schedule_flush: Callable[[], None] | None = None,
    ) -> None:
        self.dirty = dirty
        self.callback = callback
        self.schedule_flush = schedule_flush
        self._flush_requested = False
        self._lock = threading.Lock()

    def request(self) -> None:
        """Request one coalesced flush from the owning runtime."""

        if self.schedule_flush is None:
            return

        with self._lock:
            if self._flush_requested:
                return

            self._flush_requested = True

        self.schedule_flush()

    def flush(self) -> None:
        with self._lock:
            self._flush_requested = False

        nodes = self.dirty.begin_flush()

        errors = []
        try:
            for node in nodes:
                try:
                    self.callback(node)
                except Exception as exc:
                    errors.append((node, exc))
        finally:
            self.dirty.end_flush()

        if errors:
            first_node, first_exc = errors[0]
            raise RuntimeError(
                f"Scheduler callback failed for {first_node}: {first_exc}"
            ) from first_exc
