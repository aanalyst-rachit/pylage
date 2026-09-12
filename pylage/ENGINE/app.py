from __future__ import annotations

from pathlib import Path
import time
import webbrowser

from pylage.ENGINE.core.component import Component
from pylage.UI.layout.column import column
from pylage.ENGINE.routing import Router, RoutingRuntime
from pylage.ENGINE.runtime import Runtime


def run(
    app: Component | None = None,
    *,
    pages_dir: str | Path | None = None,
    title: str = "PyLage App",
    output: str | Path = "index.html",
    serve: bool = False,
    host: str = "127.0.0.1",
    port: int = 0,
    open_browser: bool = True,
) -> Path:
    """
    Render and optionally serve a PyLage application.

    Default behavior remains file-only rendering.

    When serve=True, the local runtime starts and the process
    remains alive until interrupted with Ctrl+C.
    """

    if app is not None and pages_dir is not None:
        raise TypeError(
            "pylage.run() accepts either app or pages_dir, not both."
        )

    routing_runtime: RoutingRuntime | None = None

    if pages_dir is not None:
        router = Router(pages_dir)
        root = column()
        routing_runtime = RoutingRuntime(router, root)
        routing_runtime.navigate("/")
        app = root
    elif not isinstance(app, Component):
        raise TypeError(
            "pylage.run() expects a Component root or pages_dir."
        )

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
