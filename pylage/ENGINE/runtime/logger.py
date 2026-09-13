from __future__ import annotations

import logging
import sys

LOGGER = logging.getLogger("pylage")


def log_event(
    level: int,
    event: str,
    *,
    session_id: str | None = None,
    component_id: str | None = None,
    error: BaseException | str | None = None,
    lifecycle: str | None = None,
    **fields: object,
) -> None:
    """Emit a structured PyLage runtime log record."""
    extra = {
        "event": event,
        "session_id": session_id,
        "component_id": component_id,
        "error": str(error) if error is not None else None,
        "lifecycle": lifecycle,
        **fields,
    }
    LOGGER.log(level, event, extra=extra)


def configure_logging() -> None:
    """Configure human-readable structured logging for the CLI."""
    if not any(getattr(handler, "_pylage_handler", False) for handler in LOGGER.handlers):
        handler = logging.StreamHandler(sys.stderr)
        handler._pylage_handler = True
        handler.setFormatter(
            logging.Formatter(
                "%(levelname)s event=%(event)s lifecycle=%(lifecycle)s "
                "session_id=%(session_id)s component_id=%(component_id)s "
                "error=%(error)s"
            )
        )
        LOGGER.addHandler(handler)

    LOGGER.setLevel(logging.INFO)
    LOGGER.propagate = False
