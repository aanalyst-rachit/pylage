import logging

import pytest

from pylage.ENGINE import Column, Heading
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.dirty import DirtyNodes
from pylage.ENGINE.core.scheduler import Scheduler
from pylage.ENGINE.runtime.logger import configure_logging, log_event
from pylage.ENGINE.runtime.runtime import Runtime


def test_log_event_exposes_structured_fields(caplog):
    component = Component(type="Heading")

    with caplog.at_level(logging.INFO, logger="pylage"):
        log_event(
            logging.INFO,
            "test.event",
            session_id="session-123",
            component_id=component.id,
            error="test failure",
            lifecycle="test",
            request_id="request-456",
        )

    record = next(record for record in caplog.records if record.event == "test.event")

    assert record.event == "test.event"
    assert record.session_id == "session-123"
    assert record.component_id == component.id
    assert record.error == "test failure"
    assert record.lifecycle == "test"
    assert record.request_id == "request-456"


def test_scheduler_error_logs_context_and_preserves_cause(caplog):
    component = Component(type="Heading")
    dirty = DirtyNodes()
    dirty.mark(component)

    def callback(node):
        raise ValueError("scheduler callback failed")

    scheduler = Scheduler(dirty, callback)

    with caplog.at_level(logging.ERROR, logger="pylage"), pytest.raises(RuntimeError, match="Scheduler callback failed") as exc_info:
        scheduler.flush()

    assert isinstance(exc_info.value.__cause__, ValueError)
    assert str(exc_info.value.__cause__) == "scheduler callback failed"
    assert len(dirty) == 0

    record = next(
        record
        for record in caplog.records
        if record.event == "scheduler.error"
    )

    assert record.lifecycle == "error"
    assert record.component_id == component.id
    assert record.error == "scheduler callback failed"
    assert record.error_count == 1


def test_runtime_reload_logs_component_lifecycle(caplog, tmp_path):
    old_app = Column(Heading("Old App"))
    new_app = Column(Heading("New App"))
    runtime = Runtime(old_app, output=tmp_path / "index.html")

    with caplog.at_level(logging.INFO, logger="pylage"):
        runtime.reload_app(new_app)

    record = next(
        record
        for record in caplog.records
        if record.event == "runtime.reload"
    )

    assert record.lifecycle == "reload"
    assert record.component_id == new_app.id


def test_runtime_error_logs_error_context(caplog, tmp_path):
    runtime = Runtime(
        Column(Heading("App")),
        output=tmp_path / "index.html",
    )

    with caplog.at_level(logging.ERROR, logger="pylage"):
        runtime.notify_error("development failure")

    record = next(
        record
        for record in caplog.records
        if record.event == "runtime.error"
    )

    assert record.lifecycle == "error"
    assert record.error == "development failure"


def test_runtime_stop_logs_lifecycle(caplog, tmp_path):
    runtime = Runtime(
        Column(Heading("App")),
        output=tmp_path / "index.html",
    )

    class FakeServer:
        def stop(self):
            return None

    runtime._server = FakeServer()

    with caplog.at_level(logging.INFO, logger="pylage"):
        runtime.stop()

    record = next(
        record
        for record in caplog.records
        if record.event == "runtime.stop"
    )

    assert record.lifecycle == "stop"
    assert runtime._server is None


def test_configure_logging_is_idempotent():
    logger = logging.getLogger("pylage")
    original_handlers = list(logger.handlers)
    original_level = logger.level
    original_propagate = logger.propagate

    try:
        logger.handlers.clear()
        logger.propagate = True

        configure_logging()
        first_handlers = list(logger.handlers)

        configure_logging()
        second_handlers = list(logger.handlers)

        assert len(first_handlers) == 1
        assert second_handlers == first_handlers
        assert logger.level == logging.INFO
        assert logger.propagate is False
    finally:
        logger.handlers.clear()
        logger.handlers.extend(original_handlers)
        logger.setLevel(original_level)
        logger.propagate = original_propagate
