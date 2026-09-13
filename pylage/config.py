from __future__ import annotations

import os
from dataclasses import dataclass

_DEFAULT_HOST = "127.0.0.1"
_DEFAULT_PORT = 8000
_DEFAULT_ENV = "development"


@dataclass(frozen=True)
class EnvironmentConfig:
    """Environment-backed configuration for the PyLage CLI runtime."""

    host: str = _DEFAULT_HOST
    port: int = _DEFAULT_PORT
    environment: str = _DEFAULT_ENV

    @classmethod
    def from_env(cls) -> EnvironmentConfig:
        host = os.getenv("PYLAGE_HOST", _DEFAULT_HOST).strip()
        if not host:
            raise ValueError("PYLAGE_HOST must not be empty.")

        raw_port = os.getenv("PYLAGE_PORT")
        if raw_port is None or not raw_port.strip():
            port = _DEFAULT_PORT
        else:
            try:
                port = int(raw_port.strip())
            except ValueError as exc:
                raise ValueError(
                    "PYLAGE_PORT must be an integer."
                ) from exc

        if not 0 <= port <= 65535:
            raise ValueError(
                "PYLAGE_PORT must be between 0 and 65535."
            )

        environment = os.getenv("PYLAGE_ENV", _DEFAULT_ENV).strip().lower()
        if not environment:
            raise ValueError("PYLAGE_ENV must not be empty.")

        return cls(
            host=host,
            port=port,
            environment=environment,
        )
