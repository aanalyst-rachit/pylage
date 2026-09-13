from __future__ import annotations

import threading
from collections.abc import Callable
from pathlib import Path

from pylage.ENGINE.runtime.logger import log_event


class FileWatcher:
    """Poll a file for changes and invoke a callback."""

    def __init__(
        self,
        path: str | Path,
        callback: Callable[[], None],
        *,
        interval: float = 0.25,
        error_callback: Callable[[Exception], None] | None = None,
    ) -> None:
        self.path = Path(path).resolve()

        if not self.path.is_file():
            raise FileNotFoundError(f"Watched file not found: {self.path}")

        if not callable(callback):
            raise TypeError("FileWatcher callback must be callable.")

        if interval <= 0:
            raise ValueError("FileWatcher interval must be greater than zero.")

        if error_callback is not None and not callable(error_callback):
            raise TypeError("FileWatcher error_callback must be callable or None.")

        self.callback = callback
        self.error_callback = error_callback
        self.interval = interval
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._mtime_ns = self.path.stat().st_mtime_ns

    @property
    def running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def _watch(self) -> None:
        while not self._stop_event.wait(self.interval):
            try:
                mtime_ns = self.path.stat().st_mtime_ns
            except FileNotFoundError:
                continue

            if mtime_ns == self._mtime_ns:
                continue

            self._mtime_ns = mtime_ns

            try:
                self.callback()
            except Exception as exc:  # noqa: BLE001 - watcher callback failures must not kill the watcher thread
                if self.error_callback is not None:
                    try:
                        self.error_callback(exc)
                    except Exception as callback_exc:  # noqa: BLE001 - error callback failures must not kill the watcher thread
                        log_event(30, "watcher.error_callback_failed", error=callback_exc)
                continue

    def start(self) -> None:
        if self.running:
            raise RuntimeError("FileWatcher is already running.")

        self._stop_event.clear()
        self._mtime_ns = self.path.stat().st_mtime_ns
        self._thread = threading.Thread(
            target=self._watch,
            name=f"pylage-watcher-{self.path.name}",
            daemon=True,
        )
        self._thread.start()

    def stop(self) -> None:
        thread = self._thread
        if thread is None:
            return

        self._stop_event.set()
        thread.join(timeout=max(self.interval * 4, 1.0))
        self._thread = None

    def __enter__(self) -> FileWatcher:  # noqa: PYI034 - concrete return type preserves Python 3.10 support
        self.start()
        return self

    def __exit__(self, *args: object) -> None:
        self.stop()
