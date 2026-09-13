import threading
import time

import pytest

from pylage.ENGINE.runtime.watcher import FileWatcher


def _wait_for(predicate, timeout=2.0):
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.01)

    return predicate()


def test_file_watcher_detects_file_change(tmp_path):
    target = tmp_path / "app.py"
    target.write_text("value = 1\n", encoding="utf-8")

    calls = []
    watcher = FileWatcher(
        target,
        lambda: calls.append("changed"),
        interval=0.02,
    )

    try:
        watcher.start()
        assert watcher.running

        time.sleep(0.03)
        target.write_text("value = 2\n", encoding="utf-8")

        assert _wait_for(lambda: calls == ["changed"])
    finally:
        watcher.stop()

    assert not watcher.running


def test_file_watcher_does_not_trigger_without_change(tmp_path):
    target = tmp_path / "app.py"
    target.write_text("value = 1\n", encoding="utf-8")

    calls = []
    watcher = FileWatcher(
        target,
        lambda: calls.append("changed"),
        interval=0.02,
    )

    try:
        watcher.start()
        time.sleep(0.12)
    finally:
        watcher.stop()

    assert calls == []


def test_file_watcher_stop_is_idempotent(tmp_path):
    target = tmp_path / "app.py"
    target.write_text("value = 1\n", encoding="utf-8")

    watcher = FileWatcher(target, lambda: None, interval=0.02)

    watcher.stop()
    watcher.start()
    watcher.stop()
    watcher.stop()

    assert not watcher.running


def test_file_watcher_rejects_invalid_configuration(tmp_path):
    target = tmp_path / "app.py"
    target.write_text("value = 1\n", encoding="utf-8")

    with pytest.raises(TypeError, match="callback"):
        FileWatcher(target, "not-callable")

    with pytest.raises(ValueError, match="greater than zero"):
        FileWatcher(target, lambda: None, interval=0)

    with pytest.raises(FileNotFoundError, match="Watched file not found"):
        FileWatcher(tmp_path / "missing.py", lambda: None)


def test_file_watcher_callback_failure_does_not_kill_watcher(tmp_path):
    target = tmp_path / "app.py"
    target.write_text("value = 1\n", encoding="utf-8")

    calls = []
    lock = threading.Lock()

    def callback():
        with lock:
            calls.append("changed")
        raise RuntimeError("reload failed")

    watcher = FileWatcher(target, callback, interval=0.02)

    try:
        watcher.start()

        target.write_text("value = 2\n", encoding="utf-8")
        assert _wait_for(lambda: len(calls) >= 1)

        target.write_text("value = 3\n", encoding="utf-8")
        assert _wait_for(lambda: len(calls) >= 2)

        assert watcher.running
    finally:
        watcher.stop()
