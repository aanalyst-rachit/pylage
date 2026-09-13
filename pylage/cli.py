from __future__ import annotations

import argparse
import importlib.util
import os
import sys
import time
import traceback
import webbrowser
from pathlib import Path

from pylage.config import EnvironmentConfig
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.runtime.logger import configure_logging, log_event
from pylage.ENGINE.runtime.runtime import Runtime
from pylage.ENGINE.runtime.watcher import FileWatcher


def _load_module(path: Path):
    if not path.is_file():
        raise FileNotFoundError(f'Application file not found: {path}')

    module_name = f'pylage_app_{path.stem}'
    spec = importlib.util.spec_from_file_location(module_name, path)

    if spec is None or spec.loader is None:
        raise ImportError(f'Unable to load application file: {path}')

    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent.resolve()))

    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)

    return module


def _resolve_app(path: Path) -> Component:
    module = _load_module(path)

    factory = getattr(module, 'get_app', None)
    if callable(factory):
        app = factory()
    else:
        app = getattr(module, 'app', None)

    if not isinstance(app, Component):
        raise TypeError(
            f'{path} must define get_app() returning a Component '
            'or a module-level app Component.'
        )

    return app


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='pylage',
        description='Run a PyLage application.',
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    run_parser = subparsers.add_parser(
        'run',
        help='Run a PyLage application.',
    )
    run_parser.add_argument(
        'app',
        type=Path,
        help='Python application file.',
    )
    run_parser.add_argument(
        '--host',
        default=None,
        help='Host to bind the development server. Overrides PYLAGE_HOST.',
    )
    run_parser.add_argument(
        '--port',
        type=int,
        default=None,
        help='Port to bind the development server. Overrides PYLAGE_PORT.',
    )
    run_parser.add_argument(
        '--no-browser',
        action='store_true',
        help='Do not open a browser automatically.',
    )
    run_parser.add_argument(
        '--no-reload',
        action='store_true',
        help='Disable automatic application reload on file changes.',
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == 'run':
        configure_logging()
        try:
            config = EnvironmentConfig.from_env()
        except ValueError as exc:
            parser.error(str(exc))

        app_path = args.app.resolve()
        app = _resolve_app(app_path)

        host = args.host if args.host is not None else config.host
        port = args.port if args.port is not None else config.port

        production_port = os.environ.get("PORT")
        production_mode = (
            production_port is not None
            and host == "0.0.0.0"
            and port == int(production_port)
        )

        if production_mode:
            from pylage.ENGINE.runtime.granian import GranianRuntime

            os.environ["PYLAGE_APP_FILE"] = str(app_path)
            runtime = GranianRuntime(
                "pylage.ENGINE.runtime.granian:create_application_from_file",
                host=host,
                port=port,
            )
            runtime.start()
            try:
                while runtime.running:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                pass
            finally:
                runtime.stop()
            return 0

        runtime = Runtime(
            app,
            host=host,
            port=port,
        )
        runtime.start()

        watcher = None
        try:
            if not args.no_browser:
                webbrowser.open(runtime.url)

            if not args.no_reload:
                def reload_app() -> None:
                    fresh_app = _resolve_app(app_path)
                    runtime.reload_app(fresh_app)

                def reload_error(exc: Exception) -> None:
                    log_event(
                        40,
                        "runtime.reload.error",
                        lifecycle="error",
                        error=exc,
                    )
                    print(
                        f"[PyLage] Reload failed: {exc}",
                        file=sys.stderr,
                    )
                    traceback.print_exception(
                        type(exc),
                        exc,
                        exc.__traceback__,
                        file=sys.stderr,
                    )
                    runtime.notify_error(str(exc))

                watcher = FileWatcher(
                    app_path,
                    reload_app,
                    error_callback=reload_error,
                )
                watcher.start()

            try:
                while runtime.running:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                pass
        finally:
            if watcher is not None:
                watcher.stop()
            runtime.stop()

        return 0

    parser.error(f'Unknown command: {args.command}')
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
