from pathlib import Path
import importlib
import inspect

from playwright.sync_api import sync_playwright
from pylage.ENGINE.runtime import Runtime


APP_DIR = Path("demo")
OUTPUT_DIR = Path("test_output/all_manuals")


def discover_manuals():
    return sorted(
        path.stem
        for path in APP_DIR.glob("demo_*.py")
        if path.name != "__init__.py"
    )


def test_all_manuals_smoke():
    manuals = discover_manuals()

    assert manuals, "No demo_*.py files found."

    results = []

    print()
    print("=" * 72)
    print("PYLAGE — ALL MANUALS BROWSER SMOKE TEST")
    print("=" * 72)
    print(f"Manuals discovered: {len(manuals)}")
    print()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        for manual_name in manuals:
            print(f"[TEST] {manual_name}")

            runtime = None

            try:
                module = importlib.import_module(f"demo.{manual_name}")

                get_app = getattr(module, "get_app", None)

                if get_app is None or not callable(get_app):
                    raise AssertionError("get_app() not found")

                app = get_app()

                output = OUTPUT_DIR / manual_name / "index.html"

                runtime = Runtime(
                    app,
                    title=f"PyLage Manual — {manual_name}",
                    output=str(output),
                )

                url = runtime.start()

                page = browser.new_page()

                try:
                    page.goto(url, wait_until="domcontentloaded")

                    # Give the client a short window to establish WebSocket.
                    page.wait_for_timeout(300)

                    # Basic DOM/render check.
                    root_count = page.locator("[data-pylage-id]").count()

                    if root_count == 0:
                        raise AssertionError(
                            "No PyLage components found in browser DOM"
                        )

                    # Check that the generated page has the PyLage client.
                    has_pylage_client = page.evaluate(
                        "() => !!window.PyLage"
                    )

                    if not has_pylage_client:
                        raise AssertionError(
                            "window.PyLage is missing"
                        )

                    # Check interactive components.
                    interactive = page.locator(
                        "[data-pylage-events]"
                    )
                    interactive_count = interactive.count()

                    # Basic event smoke test:
                    # click only elements explicitly advertising click events.
                    clickables = page.locator(
                        '[data-pylage-events~="click"]'
                    )

                    clicked = 0

                    for index in range(min(clickables.count(), 5)):
                        try:
                            element = clickables.nth(index)

                            if element.is_visible():
                                element.click(
                                    timeout=1500,
                                    force=True,
                                )
                                clicked += 1
                        except Exception:
                            # One problematic control should not prevent
                            # the rest of the manual from being checked.
                            pass

                    results.append(
                        (
                            manual_name,
                            "PASS",
                            root_count,
                            interactive_count,
                            clicked,
                            "",
                        )
                    )

                    print(
                        f"  PASS | components={root_count} "
                        f"interactive={interactive_count} "
                        f"clicked={clicked}"
                    )

                finally:
                    page.close()

            except Exception as exc:
                results.append(
                    (
                        manual_name,
                        "FAIL",
                        0,
                        0,
                        0,
                        f"{type(exc).__name__}: {exc}",
                    )
                )

                print(f"  FAIL | {type(exc).__name__}: {exc}")

            finally:
                if runtime is not None:
                    runtime.stop()

        browser.close()

    print()
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)

    passed = [r for r in results if r[1] == "PASS"]
    failed = [r for r in results if r[1] == "FAIL"]

    for name, status, components, interactive, clicked, error in results:
        if status == "PASS":
            print(
                f"PASS  {name:<38} "
                f"components={components:<4} "
                f"interactive={interactive:<4} "
                f"clicked={clicked}"
            )
        else:
            print(f"FAIL  {name:<38} {error}")

    print()
    print(f"TOTAL : {len(results)}")
    print(f"PASS  : {len(passed)}")
    print(f"FAIL  : {len(failed)}")
    print("=" * 72)

    assert not failed, (
        f"{len(failed)} manual(s) failed browser smoke test"
    )
