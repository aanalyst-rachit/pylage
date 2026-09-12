from __future__ import annotations

from typing import Any, Callable, Iterator

ReactiveListSubscriber = Callable[[dict[str, Any]], None]


class ReactiveList:
    """Observable list that emits one atomic delta per mutation."""

    def __init__(self, values=()):
        self._items = list(values)
        self._subscribers: list[ReactiveListSubscriber] = []

    @property
    def value(self) -> list[Any]:
        """Return a snapshot of the current list."""
        return list(self._items)

    def subscribe(self, callback: ReactiveListSubscriber) -> Callable[[], None]:
        if not callable(callback):
            raise TypeError("subscriber must be callable")
        self._subscribers.append(callback)
        def unsubscribe() -> None:
            if callback in self._subscribers:
                self._subscribers.remove(callback)
        return unsubscribe

    def bind(self, callback: ReactiveListSubscriber) -> Callable[[], None]:
        """Bind a callback to list deltas."""
        return self.subscribe(callback)

    def _notify(self, delta: dict[str, Any]) -> None:
        for subscriber in tuple(self._subscribers):
            subscriber(delta)

    def append(self, value: Any) -> None:
        index = len(self._items)
        self._items.append(value)
        self._notify({"type": "append", "index": index, "value": value})

    def remove(self, value: Any) -> None:
        index = self._items.index(value)
        self._items.pop(index)
        self._notify({"type": "remove", "index": index, "value": value})

    def insert(self, index: int, value: Any) -> None:
        size = len(self._items)
        if index < 0:
            actual_index = max(size + index, 0)
        else:
            actual_index = min(index, size)
        self._items.insert(index, value)
        self._notify({"type": "insert", "index": actual_index, "value": value})

    def move(self, from_index: int, to_index: int) -> None:
        size = len(self._items)
        if not -size <= from_index < size:
            raise IndexError("ReactiveList move index out of range")
        if not -size <= to_index < size:
            raise IndexError("ReactiveList move index out of range")
        from_index = from_index % size
        to_index = to_index % size
        if from_index == to_index:
            return
        value = self._items.pop(from_index)
        self._items.insert(to_index, value)
        self._notify({"type": "move", "from_index": from_index, "to_index": to_index, "value": value})

    def update(self, index: int, value: Any) -> None:
        old_value = self._items[index]
        try:
            unchanged = bool(old_value == value)
        except (ValueError, TypeError):
            unchanged = old_value is value
        if unchanged:
            return
        self._items[index] = value
        self._notify({"type": "update", "index": index, "old_value": old_value, "value": value})

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[Any]:
        return iter(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def __repr__(self) -> str:
        return f"ReactiveList({self._items!r})"
