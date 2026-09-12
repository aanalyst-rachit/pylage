from __future__ import annotations


class StyleCollector:
    """Collect and deduplicate CSS blocks during a render."""

    def __init__(self) -> None:
        self._styles: list[tuple[str, str]] = []
        self._seen: set[tuple[str, str]] = set()

    def clear(self) -> None:
        self._styles.clear()
        self._seen.clear()

    def add(self, css: str, attributes: str = "") -> None:
        if not css:
            return

        key = (attributes, css)
        if key in self._seen:
            return

        self._seen.add(key)
        self._styles.append(key)

    def render(self) -> str:
        return "".join(
            f"<style{attributes}>{css}</style>"
            for attributes, css in self._styles
        )

    def __len__(self) -> int:
        return len(self._styles)
