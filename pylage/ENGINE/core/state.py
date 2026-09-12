from __future__ import annotations

from typing import Any, Callable


Subscriber = Callable[[Any, Any], None]


class CircularStateDependencyError(RuntimeError):
    """Raised when a State.set() call re-enters the same State mid-notification."""


class State:
    """Reactive state value used by the pylage runtime."""

    def __init__(self, value: Any = None):
        self._value = value
        self._subscribers: list[Subscriber] = []
        self._notifying = False

    @property
    def value(self) -> Any:
        return self._value

    def set(self, value: Any) -> None:
        old_value = self._value

        try:
            unchanged = bool(old_value == value)
        except (ValueError, TypeError):
            # Fallback for types whose equality is ambiguous (e.g., NumPy arrays)
            unchanged = old_value is value

        if unchanged:
            return

        if self._notifying:
            raise CircularStateDependencyError(
                "State.set() was called re-entrantly on the same State "
                "instance while it was still notifying subscribers. "
                "This indicates a circular dependency between States — "
                "break the cycle instead of chaining .set() calls in subscribers."
            )

        self._value = value
        self._notifying = True
        try:
            for subscriber in tuple(self._subscribers):
                subscriber(old_value, value)
        finally:
            self._notifying = False

    def bind(self, callback: Subscriber) -> Callable[[], None]:
        """Bind a callback to State changes and return an unsubscribe function."""
        return self.subscribe(callback)

    def subscribe(self, callback: Subscriber) -> Callable[[], None]:
        if not callable(callback):
            raise TypeError("subscriber must be callable")

        self._subscribers.append(callback)

        def unsubscribe() -> None:
            if callback in self._subscribers:
                self._subscribers.remove(callback)

        return unsubscribe

    def __repr__(self) -> str:
        return f"State({self._value!r})"


class DerivedState(State):
    """Read-only reactive state derived from one or more source States."""

    def __init__(self, *sources: State, compute: Callable[..., Any]):
        if not sources:
            raise ValueError("DerivedState requires at least one source State")
        if not callable(compute):
            raise TypeError("compute must be callable")
        if any(not isinstance(source, State) for source in sources):
            raise TypeError("all DerivedState sources must be State instances")

        self._sources = tuple(sources)
        self._compute = compute
        self._source_unsubscribers: list[Callable[[], None]] = []
        self._disposed = False

        initial = self._compute(*(source.value for source in self._sources))
        super().__init__(initial)

        for source in self._sources:
            self._source_unsubscribers.append(
                source.subscribe(self._source_changed)
            )

    def _source_changed(self, _old: Any, _new: Any) -> None:
        if self._disposed:
            return
        value = self._compute(*(source.value for source in self._sources))
        super().set(value)

    def set(self, value: Any) -> None:
        raise TypeError("DerivedState is read-only; change its source State instead")

    def dispose(self) -> None:
        if self._disposed:
            return
        for unsubscribe in self._source_unsubscribers:
            unsubscribe()
        self._source_unsubscribers.clear()
        self._disposed = True

