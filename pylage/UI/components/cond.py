from __future__ import annotations

from typing import Any

from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.state import State


class Cond(Component):
    """Conditionally render one of two reactive component branches."""

    def __init__(
        self,
        condition: State,
        true_branch: Any,
        false_branch: Any = None,
        *extra_branches: Any,
    ) -> None:
        if not isinstance(condition, State):
            raise TypeError("condition must be a State instance")

        if extra_branches:
            raise TypeError("branches must contain at most two components")

        if false_branch is not None and not isinstance(false_branch, Component):
            raise TypeError("branches must be Component instances")

        if true_branch is not None and not isinstance(true_branch, Component):
            raise TypeError("branches must be Component instances")

        self._condition = condition
        self._true_branch = true_branch
        self._false_branch = false_branch
        self._condition_unsubscribe = None
        self._disposed = False

        initial_children = self._children_for(condition.value)

        super().__init__(
            type="cond",
            children=initial_children,
        )

        self._condition_unsubscribe = condition.subscribe(
            self._condition_changed
        )

    def _children_for(self, value: Any) -> list[Component]:
        branch = (
            self._true_branch
            if bool(value)
            else self._false_branch
        )

        if branch is None:
            return []

        return [branch]

    def _condition_changed(self, _old: Any, new: Any) -> None:
        if self._disposed:
            return

        self.set_children(*self._children_for(new))

    def dispose(self) -> None:
        """Stop reacting to condition changes."""
        if self._disposed:
            return

        if self._condition_unsubscribe is not None:
            self._condition_unsubscribe()
            self._condition_unsubscribe = None

        self._disposed = True


def cond(
    condition: State,
    true_branch: Any,
    false_branch: Any = None,
) -> Cond:
    """Create a reactive conditional component."""
    return Cond(condition, true_branch, false_branch)


__all__ = ["Cond", "cond"]
