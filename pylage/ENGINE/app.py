from __future__ import annotations

import time
import webbrowser
from collections.abc import Callable
from pathlib import Path

from pylage.ENGINE.core.component import Component
from pylage.ENGINE.routing import Router, RoutingRuntime
from pylage.ENGINE.runtime import EmbeddedGranianRuntime, Runtime
from pylage.ENGINE.runtime.asgi import ASGIApp
from pylage.UI.layout.column import column


def run(
    app: Component | None = None,
    *,
    app_factory: Callable[[], Component] | None = None,
    pages_dir: str | Path | None = None,
    title: str = "PyLage App",
    output: str | Path = "index.html",
    serve: bool = False,
    host: str = "127.0.0.1",
    port: int = 0,
    open_browser: bool = True,
    runtime: str = "local",
) -> Path:
    """
    Render and optionally serve a PyLage application.

    Default behavior remains file-only rendering.

    When serve=True, the local runtime starts and the process
    remains alive until interrupted with Ctrl+C.
    """

    if runtime not in {"local", "granian"}:
        raise ValueError(
            'pylage.run() runtime must be "local" or "granian".'
        )

    supplied = sum(value is not None for value in (app, app_factory, pages_dir))
    if supplied > 1:
        raise TypeError(
            "pylage.run() accepts only one of app, app_factory, or pages_dir."
        )

    routing_runtime: RoutingRuntime | None = None

    if pages_dir is not None:
        router = Router(pages_dir)
        root = column()
        routing_runtime = RoutingRuntime(router, root)
        routing_runtime.navigate("/")
        app = root
    elif app_factory is not None:
        if not callable(app_factory):
            raise TypeError("pylage.run() expects app_factory to be callable.")
    elif not isinstance(app, Component):
        raise TypeError(
            "pylage.run() expects a Component root, app_factory, or pages_dir."
        )

    if runtime == "granian" and app_factory is None:
        if pages_dir is not None:
            asgi = ASGIApp(pages_dir=pages_dir)
            template = asgi.template
        else:
            if not isinstance(app, Component):
                raise TypeError(
                    "pylage.run() expects a Component root, app_factory, or pages_dir."
                )
            asgi = ASGIApp(root=app)
            template = app

        from pylage.ENGINE.renderers.html import render_document

        document = render_document(
            template,
            title=title,
        )

        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(document, encoding="utf-8")

        if not serve:
            return output_path

        runtime_backend = EmbeddedGranianRuntime(
            asgi,
            host=host,
            port=port,
        )
        url = runtime_backend.start()

        print(f"PyLage app running at {url}")
        print("Press Ctrl+C to stop.")

        if open_browser:
            webbrowser.open(url)

        try:
            while True:
                time.sleep(0.25)
        except KeyboardInterrupt:
            print("\nStopping PyLage...")
        finally:
            runtime_backend.stop()

        return output_path

    if app_factory is not None:
        template = app_factory()
        if not isinstance(template, Component):
            raise TypeError("pylage.run() app_factory must return a Component.")

        from pylage.ENGINE.renderers.html import render_document

        document = render_document(
            template,
            title=title,
        )

        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            document,
            encoding="utf-8",
        )

        if not serve:
            return output_path

        asgi = ASGIApp(
            app_factory=app_factory,
            document=document,
            template=template,
        )
        runtime = EmbeddedGranianRuntime(
            asgi,
            host=host,
            port=port,
        )
        url = runtime.start()

        print(f"PyLage app running at {url}")
        print("Press Ctrl+C to stop.")

        if open_browser:
            webbrowser.open(url)

        try:
            while True:
                time.sleep(0.25)
        except KeyboardInterrupt:
            print("\nStopping PyLage...")
        finally:
            runtime.stop()

        return output_path

    if not serve:
        from pylage.ENGINE.renderers.html import render_document

        document = render_document(
            app,
            title=title,
        )

        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            document,
            encoding="utf-8",
        )

        return output_path

    navigation_handler = None
    if routing_runtime is not None:
        def navigation_handler(path: str) -> None:
            routing_runtime.navigate(path)

    runtime = Runtime(
        app,
        title=title,
        output=output,
        host=host,
        port=port,
        navigation_handler=navigation_handler,
    )

    output_path = runtime.render()
    url = runtime.start()

    print(f"PyLage app running at {url}")
    print("Press Ctrl+C to stop.")

    if open_browser:
        webbrowser.open(url)

    try:
        while True:
            time.sleep(0.25)
    except KeyboardInterrupt:
        print("\nStopping PyLage...")

    finally:
        runtime.stop()

    return output_path
