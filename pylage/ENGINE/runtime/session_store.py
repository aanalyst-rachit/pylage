from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class _SessionEntry:
    session: Any
    expires_at: float


class SessionStore:
    """Swappable interface for runtime session storage."""

    def get(self, token: str) -> Any | None:
        raise NotImplementedError

    def put(self, token: str, session: Any) -> None:
        raise NotImplementedError

    def remove(self, token: str) -> Any | None:
        raise NotImplementedError

    def evict_expired(self) -> list[tuple[str, Any]]:
        raise NotImplementedError

    def clear(self) -> list[tuple[str, Any]]:
        raise NotImplementedError


class InMemorySessionStore(SessionStore):
    """In-memory session store with inactivity-based TTL eviction."""

    DEFAULT_TTL = 300.0

    def __init__(
        self,
        ttl: float = DEFAULT_TTL,
        *,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if ttl <= 0:
            raise ValueError("ttl must be greater than zero.")
        self.ttl = float(ttl)
        self._clock = clock
        self._entries: dict[str, _SessionEntry] = {}

    def put(self, token: str, session: Any) -> None:
        self._entries[token] = _SessionEntry(
            session=session,
            expires_at=self._clock() + self.ttl,
        )

    def get(self, token: str) -> Any | None:
        entry = self._entries.get(token)
        if entry is None:
            return None

        if entry.expires_at <= self._clock():
            self._entries.pop(token, None)
            return None

        entry.expires_at = self._clock() + self.ttl
        return entry.session

    def remove(self, token: str) -> Any | None:
        entry = self._entries.pop(token, None)
        return None if entry is None else entry.session

    def evict_expired(self) -> list[tuple[str, Any]]:
        now = self._clock()
        expired: list[tuple[str, Any]] = []

        for token, entry in tuple(self._entries.items()):
            if entry.expires_at <= now:
                self._entries.pop(token, None)
                expired.append((token, entry.session))

        return expired

    def clear(self) -> list[tuple[str, Any]]:
        entries = [(token, entry.session) for token, entry in self._entries.items()]
        self._entries.clear()
        return entries
