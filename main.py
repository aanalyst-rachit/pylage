from __future__ import annotations

import importlib
import inspect
import os
import sys
import threading
import time
from pathlib import Path

import webview

BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from pylage import run
from pylage.ENGINE import Button, Card, Column, Heading, Row, State, Text
from pylage.ENGINE.styling.style import Style


DEMO_DIR = BASE_DIR / "demo"

MANUALS: dict[str, object] = {}
MANUAL_APPS: dict[str, object] = {}


def display_name_from_path(path: Path) -> str:
    name = path.stem.removeprefix("demo_")
    return name.replace("_", " ").strip().title()


def discover_manuals() -> dict[str, object]:
    manuals: dict[str, object] = {}

    if not DEMO_DIR.exists():
        return manuals

    for path in sorted(DEMO_DIR.glob("demo_*.py")):
        module_name = f"demo.{path.stem}"

        try:
            if module_name in sys.modules:
                module = importlib.reload(sys.modules[module_name])
            else:
                module = importlib.import_module(module_name)
        except Exception as exc:
            print(f"[DISCOVERY ERROR] {path.name}: {exc}")
            continue

        get_app = getattr(module, "get_app", None)

        if not callable(get_app):
            continue

        try:
            signature = inspect.signature(get_app)

            required_parameters = [
                parameter
                for parameter in signature.parameters.values()
                if parameter.default is inspect.Parameter.empty
                and parameter.kind
                in (
                    inspect.Parameter.POSITIONAL_ONLY,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.KEYWORD_ONLY,
                )
            ]

            if required_parameters:
                print(
                    f"[DISCOVERY SKIP] {path.name}: "
                    f"get_app() requires arguments"
                )
                continue

        except (TypeError, ValueError) as exc:
            print(f"[DISCOVERY SKIP] {path.name}: {exc}")
            continue

        display_name = display_name_from_path(path)
        manuals[display_name] = module

    return dict(
        sorted(
            manuals.items(),
            key=lambda item: item[0].lower(),
        )
    )


def build_manual_cache(manuals: dict[str, object]) -> dict[str, object]:
    apps: dict[str, object] = {}

    print()
    print("============================================================")
    print("BUILDING MANUAL APP CACHE")
    print("============================================================")

    for name, module in manuals.items():
        try:
            app = module.get_app() # type: ignore
            apps[name] = app
            print(f"[CACHE OK] {name}")
        except Exception as exc:
            print(f"[CACHE ERROR] {name}: {exc}")

    print("============================================================")
    print(f"[CACHE] Built {len(apps)} manual apps")
    print("============================================================")
    print()

    return apps


def get_manuals() -> dict[str, object]:
    global MANUALS
    MANUALS = discover_manuals()
    return MANUALS


def get_manual_apps() -> dict[str, object]:
    global MANUAL_APPS

    if not MANUALS:
        get_manuals()

    MANUAL_APPS = build_manual_cache(MANUALS)
    return MANUAL_APPS


def manual_error_view(name: str, error: Exception) -> Column: # type: ignore
    return Column(
        Heading(
            f"Failed to load: {name}",
            level=2,
        ),
        Text(
            f"{type(error).__name__}: {error}",
        ),
        style=Style(
            width="100%",
            height="100%",
            padding="1.5rem",
            box_sizing="border-box",
        ),
    )


def build_manual_browser() -> Column: # type: ignore
    manuals = get_manuals()
    manual_apps = get_manual_apps()

    manual_names = [
        name
        for name in manuals
        if name in manual_apps
    ]

    print(f"[DISCOVERY] Found {len(manuals)} manuals")
    print(f"[CACHE] Usable {len(manual_apps)} manuals")

    if not manual_names:
        return Column(
            Text("No usable manuals found."),
            style=Style(
                width="100vw",
                height="100vh",
                box_sizing="border-box",
            ),
        )

    selected_name = State(manual_names[0])

    initial_app = manual_apps[manual_names[0]]

    content_area = Column(
        initial_app,
        style=Style(
            width="100%",
            height="100%",
            overflow="auto",
            padding="1.5rem",
            box_sizing="border-box",
        ),
    )

    def select_manual(name: str):
        def handler(payload=None):
            print(f"[MANUAL CLICK] {name}")
            selected_name.set(name)

        return handler

    def refresh_content(old_name, new_name):
        print(
            f"[MANUAL SWITCH] "
            f"{old_name!r} -> {new_name!r}"
        )

        if new_name not in manual_apps:
            print(
                f"[MANUAL SWITCH] Unknown cached manual: "
                f"{new_name}"
            )
            return

        app_instance = manual_apps[new_name]

        print(
            f"[MANUAL MOUNT] "
            f"{new_name} "
            f"instance_id={getattr(app_instance, 'id', None)}"
        )

        content_area.set_children(
            app_instance
        )

    selected_name.subscribe(refresh_content)

    sidebar_items = [
        Card(
            Text(
                name,
                style=Style(
                    font_weight="600",
                ),
            ),
            on_click=select_manual(name),
            style=Style(
                padding="0.75rem",
                margin_bottom="0.5rem",
                border="1px solid #e2e8f0",
                border_radius="0.5rem",
                cursor="pointer",
            ),
        )
        for name in manual_names
    ]

    sidebar = Column(
        Heading(
            "Manuals",
            level=3,
        ),
        Column(
            *sidebar_items,
        ),
        style=Style(
            width="280px",
            height="100%",
            padding="1rem",
            background_color="#f8fafc",
            border_right="1px solid #e2e8f0",
            overflow="auto",
            flex_shrink="0",
            box_sizing="border-box",
        ),
    )

    def on_refresh_click(payload=None):
        print("[REFRESH] Reloading window and re-discovering manuals...")
        get_manuals()
        get_manual_apps()
        if window_instance:
            window_instance.load_url("http://127.0.0.1:8080")

    header = Row(
        Heading(
            "⚡ PyLage Manual Browser",
            level=2,
            style=Style(
                margin="0",
            ),
        ),
        Button(
            "🔄 Refresh",
            on_click=on_refresh_click,
            style=Style(
                padding="0.4rem 0.8rem",
                cursor="pointer",
                border_radius="0.375rem",
                border="1px solid #cbd5e1",
                background_color="#ffffff",
            ),
        ),
        style=Style(
            width="100%",
            height="50px",
            min_height="50px",
            max_height="50px",
            padding="0 1rem",
            align_items="center",
            justify_content="space-between",
            border_bottom="1px solid #e2e8f0",
            flex_shrink="0",
            box_sizing="border-box",
        ),
    )

    body = Row(
        sidebar,
        content_area,
        style=Style(
            width="100%",
            height="calc(100vh - 50px)",
            flex="1",
            min_height="0",
            overflow="hidden",
            box_sizing="border-box",
        ),
    )

    return Column(
        header,
        body,
        style=Style(
            position="fixed",
            top="0",
            left="0",
            right="0",
            bottom="0",
            width="100vw",
            height="100vh",
            margin="0",
            padding="0",
            overflow="hidden",
            box_sizing="border-box",
        ),
    )


def get_app() -> Column: # type: ignore
    return build_manual_browser()


def start_pylage():
    run(
        get_app(),
        title="PyLage Manual",
        output=Path("index.html"),
        serve=True,
        host="127.0.0.1",
        port=8080,
        open_browser=False,
    )


window_instance = None

if __name__ == "__main__":
    server_thread = threading.Thread(
        target=start_pylage,
        daemon=True,
    )

    server_thread.start()

    time.sleep(1)

    window_instance = webview.create_window(
        "PyLage Manual",
        "http://127.0.0.1:8080",
        width=1200,
        height=800,
    )

    webview.start(gui="qt", debug=False)