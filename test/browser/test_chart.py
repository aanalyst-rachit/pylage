from playwright.sync_api import expect, sync_playwright

import plotly.graph_objects as go

from pylage.ENGINE import Column, Dialog, Drawer, State
from pylage import Chart
from pylage.ENGINE.runtime import Runtime


def test_chart_renders_and_reacts_in_browser():
    chart_state = State(
        go.Figure(
            data=[
                go.Bar(
                    x=["A", "B"],
                    y=[10, 20],
                    name="Initial",
                )
            ]
        )
    )

    chart = Chart(
        chart_state,
        height=350,
        title="Browser Chart Test",
    )

    app = Column(chart)

    runtime = Runtime(
        app,
        title="PyLage Chart Browser Test",
        output="test_output/chart_browser/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.on(
                "console",
                lambda msg: print(
                    f"[BROWSER CONSOLE] {msg.type}: {msg.text}"
                ),
            )
            page.on(
                "pageerror",
                lambda exc: print(
                    f"[BROWSER PAGE ERROR] {exc}"
                ),
            )

            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)

            print(
                "[CHART HTML]",
                page.locator(
                    f'[data-pylage-id="{chart.id}"]'
                ).evaluate("el => el.outerHTML"),
            )

            print(
                "[PLOTLY STATE]",
                page.evaluate(
                    """
                    () => {
                        const el = document.querySelector(
                            '[data-pylage-chart="1"]'
                        );

                        return {
                            pylage: !!window.PyLage,
                            charts: !!(
                                window.PyLage &&
                                window.PyLage.charts
                            ),
                            chartUpdate: !!(
                                window.PyLage &&
                                window.PyLage.charts &&
                                typeof window.PyLage.charts.update === "function"
                            ),
                            plotly: !!window.Plotly,
                            chartCount: document.querySelectorAll(
                                '[data-pylage-chart="1"]'
                            ).length,
                            innerHTML: el ? el.innerHTML : null,
                            hasData: !!(el && el.data),
                            hasFullLayout: !!(el && el._fullLayout),
                        };
                    }
                    """
                ),
            )

            chart_locator = page.locator(
                f'[data-pylage-id="{chart.id}"]'
            )

            expect(chart_locator).to_be_visible()

            # Plotly must be mounted and contain rendered graph content.
            expect(
                chart_locator.locator(".plot-container")
            ).to_be_attached(timeout=10000)

            expect(
                chart_locator.locator(".plot-container svg.main-svg").first
            ).to_be_attached(timeout=10000)

            expect(
                chart_locator.locator(".cartesianlayer")
            ).to_be_attached(timeout=10000)

            assert page.evaluate(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );
                    return !!(
                        el &&
                        el._fullLayout &&
                        el.data &&
                        el.data.length === 1
                    );
                }
                """
            )

            initial_data = page.evaluate(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );
                    return {
                        x: el.data[0].x,
                        y: el.data[0].y
                    };
                }
                """
            )

            assert initial_data == {
                "x": ["A", "B"],
                "y": [10, 20],
            }

            # Python State -> browser differential Chart update.
            chart_state.set(
                go.Figure(
                    data=[
                        go.Bar(
                            x=["C", "D", "E"],
                            y=[30, 40, 50],
                            name="Updated",
                        )
                    ]
                )
            )

            page.wait_for_function(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );
                    return !!(
                        el &&
                        el.data &&
                        el.data[0] &&
                        el.data[0].x &&
                        el.data[0].x.length === 3 &&
                        el.data[0].x[0] === "C"
                    );
                }
                """,
                timeout=10000,
            )

            updated_data = page.evaluate(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );
                    return {
                        x: el.data[0].x,
                        y: el.data[0].y
                    };
                }
                """
            )

            assert updated_data == {
                "x": ["C", "D", "E"],
                "y": [30, 40, 50],
            }

            browser.close()

    finally:
        runtime.stop()


def test_chart_runtime_is_idempotent_and_uses_single_plotly_script():
    chart = Chart(
        go.Figure(
            data=[
                go.Bar(x=["A"], y=[1]),
            ]
        )
    )

    app = Column(chart)

    runtime = Runtime(
        app,
        title="PyLage Chart Idempotency Test",
        output="test_output/chart_browser/idempotency.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            page.wait_for_function(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );
                    return !!(
                        window.Plotly &&
                        el &&
                        el._fullLayout &&
                        el.data
                    );
                }
                """,
                timeout=10000,
            )

            result = page.evaluate(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );

                    window.PyLage.charts.mount(el);
                    window.PyLage.charts.mount(el);
                    window.PyLage.charts.scan(document);

                    return {
                        plotlyScripts: document.querySelectorAll(
                            'script[data-pylage-plotly="1"]'
                        ).length,
                        chartInstances: !!(
                            el &&
                            el._fullLayout &&
                            el.data
                        ),
                    };
                }
                """
            )

            assert result == {
                "plotlyScripts": 1,
                "chartInstances": True,
            }

            browser.close()

    finally:
        runtime.stop()


def test_chart_destroy_purges_plotly_instance():
    chart = Chart(
        go.Figure(
            data=[
                go.Bar(x=["A"], y=[1]),
            ]
        )
    )

    app = Column(chart)

    runtime = Runtime(
        app,
        title="PyLage Chart Destroy Test",
        output="test_output/chart_browser/destroy.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            page.wait_for_function(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );
                    return !!(
                        el &&
                        el._fullLayout &&
                        el.data
                    );
                }
                """,
                timeout=10000,
            )

            result = page.evaluate(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );

                    const before = !!(
                        el &&
                        el._fullLayout &&
                        el.data
                    );

                    window.PyLage.charts.destroy(el);

                    return {
                        before: before,
                        afterFullLayout: !!(
                            el &&
                            el._fullLayout
                        ),
                        afterData: !!(
                            el &&
                            el.data
                        ),
                    };
                }
                """
            )

            assert result["before"] is True
            assert result["afterFullLayout"] is False
            assert result["afterData"] is False

            browser.close()

    finally:
        runtime.stop()


def test_chart_dynamic_insert_and_remove_uses_runtime_lifecycle():
    chart = Chart(
        go.Figure(
            data=[
                go.Bar(x=["A"], y=[1]),
            ]
        )
    )

    app = Column(chart)

    runtime = Runtime(
        app,
        title="PyLage Chart Dynamic Lifecycle Test",
        output="test_output/chart_browser/dynamic.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            page.wait_for_function(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );
                    return !!(
                        window.PyLage &&
                        window.PyLage.charts &&
                        window.Plotly &&
                        el &&
                        el._fullLayout
                    );
                }
                """,
                timeout=10000,
            )

            result = page.evaluate(
                """
                () => {
                    const original = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );

                    const clone = original.cloneNode(true);
                    clone.removeAttribute("data-pylage-id");
                    clone.setAttribute(
                        "data-pylage-id",
                        "dynamic-chart-test"
                    );

                    document.body.appendChild(clone);

                    return true;
                }
                """
            )

            assert result is True

            page.wait_for_function(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-id="dynamic-chart-test"]'
                    );
                    return !!(
                        el &&
                        el._fullLayout &&
                        el.data
                    );
                }
                """,
                timeout=10000,
            )

            assert page.locator(
                '[data-pylage-id="dynamic-chart-test"]'
            ).count() == 1

            page.evaluate(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-id="dynamic-chart-test"]'
                    );
                    el.remove();
                }
                """
            )

            page.wait_for_function(
                """
                () => {
                    return !document.querySelector(
                        '[data-pylage-id="dynamic-chart-test"]'
                    );
                }
                """,
                timeout=5000,
            )

            browser.close()

    finally:
        runtime.stop()


def test_chart_browser_error_uses_pylage_error_surface():
    chart = Chart(
        go.Figure(
            data=[
                go.Bar(x=["A"], y=[1]),
            ]
        )
    )

    app = Column(chart)

    runtime = Runtime(
        app,
        title="PyLage Chart Error Test",
        output="test_output/chart_browser/error.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            result = page.evaluate(
                """
                () => {
                    const messages = [];

                    window.PyLage.onError = function (message) {
                        messages.push(String(message));
                    };

                    const el = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );

                    el.setAttribute(
                        "data-chart-payload",
                        "{invalid-json"
                    );

                    window.PyLage.charts.mount(el);

                    return messages;
                }
                """
            )

            assert result == []

            # Invalid JSON is handled by the existing payload parser.
            # It must not create a fake component event or protocol message.
            assert page.locator(
                '[data-pylage-chart="1"]'
            ).count() == 1

            browser.close()

    finally:
        runtime.stop()



def test_chart_payload_html_is_not_executed():
    chart = Chart(
        go.Figure(
            data=[
                go.Bar(x=["<img src=x onerror=\"window.__pylage_xss=1\">"], y=[1]),
            ]
        )
    )

    app = Column(chart)

    runtime = Runtime(
        app,
        title="PyLage Chart Security Test",
        output="test_output/chart_browser/security.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            result = page.evaluate(
                """
                () => ({
                    executed: window.__pylage_xss === 1,
                    scripts: document.scripts.length,
                    images: document.querySelectorAll("img").length,
                })
                """
            )

            print(result)

            browser.close()

    finally:
        runtime.stop()


def test_chart_plotly_loader_retries_after_asset_failure():
    chart = Chart(
        go.Figure(
            data=[
                go.Bar(x=["A"], y=[1]),
            ]
        )
    )

    app = Column(chart)

    runtime = Runtime(
        app,
        title="PyLage Chart Loader Retry Test",
        output="test_output/chart_browser/loader_retry.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            attempts = {"count": 0}

            def intercept_plotly(route):
                attempts["count"] += 1

                if attempts["count"] == 1:
                    route.abort()
                else:
                    route.continue_()

            page.route(
                "**/_pylage/assets/plotly.min.js",
                intercept_plotly,
            )

            page.goto(url, wait_until="domcontentloaded")

            page.wait_for_function(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );

                    return !!(
                        el &&
                        window.PyLage &&
                        window.PyLage.charts
                    );
                }
                """,
                timeout=5000,
            )

            page.wait_for_function(
                """
                () => {
                    return document.querySelectorAll(
                        'script[data-pylage-plotly="1"]'
                    ).length === 0;
                }
                """,
                timeout=10000,
            )

            assert attempts["count"] == 1
            assert page.evaluate("() => !!window.Plotly") is False

            page.evaluate(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );

                    if (!el) {
                        throw new Error("Chart element not found");
                    }

                    window.PyLage.charts.mount(el);
                }
                """
            )

            page.wait_for_function(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );

                    return !!(
                        window.Plotly &&
                        el &&
                        el._fullLayout &&
                        el.data
                    );
                }
                """,
                timeout=15000,
            )

            assert attempts["count"] == 2

            browser.close()

    finally:
        runtime.stop()

def test_chart_works_inside_nested_layouts_and_multiple_charts():
    charts = [
        Chart(
            go.Figure(
                data=[go.Bar(x=["A", "B"], y=[1, 2])]
            ),
            height=250,
        ),
        Chart(
            go.Figure(
                data=[go.Scatter(x=["A", "B"], y=[3, 4])]
            ),
            height=250,
        ),
        Chart(
            go.Figure(
                data=[go.Bar(x=["A", "B"], y=[5, 6])]
            ),
            height=250,
        ),
    ]

    app = Column(
        charts[0],
        __import__("pylage.ENGINE", fromlist=["Row"]).Row(
            __import__("pylage.ENGINE", fromlist=["Card"]).Card(charts[1]),
            charts[2],
        ),
    )

    runtime = Runtime(
        app,
        title="PyLage Chart Layout Test",
        output="test_output/chart_layout/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded")

            page.wait_for_function(
                """
                () => document.querySelectorAll(
                    '[data-pylage-chart="1"]'
                ).length === 3
                """,
                timeout=10000,
            )

            page.wait_for_function(
                """
                () => Array.from(
                    document.querySelectorAll(
                        '[data-pylage-chart="1"]'
                    )
                ).every(el => !!el._fullLayout)
                """,
                timeout=10000,
            )

            assert page.locator(
                '[data-pylage-chart="1"]'
            ).count() == 3

            assert page.locator(
                '[data-pylage-chart="1"] .plot-container'
            ).count() == 3

            browser.close()

    finally:
        runtime.stop()


def test_chart_has_accessibility_metadata():
    chart = Chart(
        go.Figure(
            data=[go.Bar(x=["A", "B"], y=[10, 20])]
        ),
        title="Sales Chart",
    )

    runtime = Runtime(
        Column(chart),
        title="PyLage Chart Accessibility Test",
        output="test_output/chart_accessibility/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded")

            locator = page.locator(
                f'[data-pylage-id="{chart.id}"]'
            )

            expect(locator).to_have_attribute(
                "role",
                "img",
            )

            expect(locator).to_have_attribute(
                "aria-label",
                "Sales Chart",
            )

            browser.close()

    finally:
        runtime.stop()



def test_chart_resize_observer_reacts_to_container_resize():
    chart = Chart(
        go.Figure(
            data=[go.Bar(x=["A", "B"], y=[10, 20])]
        ),
        width="100%",
        height=300,
    )

    runtime = Runtime(
        Column(chart),
        title="PyLage Chart Resize Test",
        output="test_output/chart_resize/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded")

            page.wait_for_function(
                """
                (id) => {
                    const el = document.querySelector(
                        `[data-pylage-id="${id}"]`
                    );
                    return !!(
                        el &&
                        el._fullLayout &&
                        el.__pylageChartResizeObserver
                    );
                }
                """,
                arg=chart.id,
                timeout=10000,
            )

            initial_width = page.evaluate(
                """
                (id) => {
                    const el = document.querySelector(
                        `[data-pylage-id="${id}"]`
                    );
                    return el.getBoundingClientRect().width;
                }
                """,
                arg=chart.id,
            )

            page.evaluate(
                """
                (id) => {
                    const el = document.querySelector(
                        `[data-pylage-id="${id}"]`
                    );
                    el.style.width = "600px";
                }
                """,
                arg=chart.id,
            )

            page.wait_for_function(
                """
                (id) => {
                    const el = document.querySelector(
                        `[data-pylage-id="${id}"]`
                    );
                    return el.getBoundingClientRect().width === 600;
                }
                """,
                arg=chart.id,
                timeout=10000,
            )

            resized_width = page.evaluate(
                """
                (id) => {
                    const el = document.querySelector(
                        `[data-pylage-id="${id}"]`
                    );
                    return el.getBoundingClientRect().width;
                }
                """,
                arg=chart.id,
            )

            assert initial_width != resized_width
            assert resized_width == 600

            browser.close()

    finally:
        runtime.stop()

def test_chart_initially_hidden_then_renders_when_visible():
    chart_visible = State(False)

    chart = Chart(
        go.Figure(
            data=[
                go.Bar(
                    x=["A", "B"],
                    y=[10, 20],
                )
            ]
        ),
        visible=chart_visible,
        height=350,
    )

    app = Column(chart)

    runtime = Runtime(
        app,
        title="PyLage Hidden Chart Test",
        output="test_output/chart_browser/hidden_chart.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            chart_locator = page.locator(
                f'[data-pylage-id="{chart.id}"]'
            )

            # The chart element exists but is initially hidden.
            expect(chart_locator).to_be_hidden()

            initial = page.evaluate(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );

                    return {
                        hidden: !!el.hidden,
                        connected: !!(
                            el &&
                            el.isConnected
                        ),
                        hasPlotlyData: !!(
                            el &&
                            el.data &&
                            el.data.length
                        ),
                    };
                }
                """
            )

            assert initial["hidden"] is True
            assert initial["connected"] is True

            # The chart should not need a browser reload.
            chart_visible.set(True)

            # Wait for the normal reactive DOM update.
            expect(chart_locator).to_be_visible(timeout=10000)

            # Once visible, Plotly must become usable.
            expect(
                chart_locator.locator(".plot-container")
            ).to_be_attached(timeout=15000)

            expect(
                chart_locator.locator(
                    ".plot-container svg.main-svg"
                ).first
            ).to_be_attached(timeout=15000)

            final = page.evaluate(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );

                    return {
                        hidden: !!el.hidden,
                        hasPlotlyData: !!(
                            el &&
                            el.data &&
                            el.data.length === 1
                        ),
                        hasFullLayout: !!(
                            el &&
                            el._fullLayout
                        ),
                        width: el && el._fullLayout
                            ? el._fullLayout.width
                            : 0,
                        height: el && el._fullLayout
                            ? el._fullLayout.height
                            : 0,
                    };
                }
                """
            )

            assert final["hidden"] is False
            assert final["hasPlotlyData"] is True
            assert final["hasFullLayout"] is True
            assert final["width"] > 0
            assert final["height"] > 0

            browser.close()

    finally:
        runtime.stop()


def test_chart_inside_dialog_renders_when_dialog_opens():
    dialog_open = State(False)

    chart = Chart(
        go.Figure(
            data=[
                go.Bar(
                    x=["A", "B"],
                    y=[10, 20],
                )
            ]
        ),
        height=350,
    )

    dialog = Dialog(
        chart,
        open=dialog_open,
    )

    app = Column(dialog)

    runtime = Runtime(
        app,
        title="PyLage Chart Dialog Test",
        output="test_output/chart_browser/chart_dialog.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            chart_locator = page.locator(
                f'[data-pylage-id="{chart.id}"]'
            )

            # Dialog starts closed.
            dialog_locator = page.locator("dialog")

            expect(
                dialog_locator
            ).not_to_be_visible()

            assert page.evaluate(
                "() => !document.querySelector('dialog').open"
            )

            # Chart must still exist in the document.
            expect(chart_locator).to_be_attached()

            # Open the dialog through the normal State pipeline.
            dialog_open.set(True)

            expect(
                dialog_locator
            ).to_be_visible(timeout=10000)

            expect(
                dialog_locator
            ).to_have_attribute("open", "")

            # Chart must become usable without page reload.
            expect(
                chart_locator.locator(".plot-container")
            ).to_be_attached(timeout=15000)

            expect(
                chart_locator.locator(
                    ".plot-container svg.main-svg"
                ).first
            ).to_be_attached(timeout=15000)

            result = page.evaluate(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );

                    return {
                        hasPlotlyData: !!(
                            el &&
                            el.data &&
                            el.data.length === 1
                        ),
                        hasFullLayout: !!(
                            el &&
                            el._fullLayout
                        ),
                        width: el && el._fullLayout
                            ? el._fullLayout.width
                            : 0,
                        height: el && el._fullLayout
                            ? el._fullLayout.height
                            : 0,
                    };
                }
                """
            )

            assert result["hasPlotlyData"] is True
            assert result["hasFullLayout"] is True
            assert result["width"] > 0
            assert result["height"] > 0

            browser.close()

    finally:
        runtime.stop()


def test_chart_inside_drawer_renders_when_drawer_opens():
    drawer_open = State(False)

    chart = Chart(
        go.Figure(
            data=[
                go.Bar(
                    x=["A", "B"],
                    y=[10, 20],
                )
            ]
        ),
        height=350,
    )

    drawer = Drawer(
        chart,
        open=drawer_open,
    )

    app = Column(drawer)

    runtime = Runtime(
        app,
        title="PyLage Chart Drawer Test",
        output="test_output/chart_browser/chart_drawer.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            chart_locator = page.locator(
                f'[data-pylage-id="{chart.id}"]'
            )

            drawer_locator = page.locator(
                '[data-pylage-id="' + drawer.id + '"]'
            )

            # Drawer starts closed.
            expect(
                drawer_locator
            ).not_to_be_visible()

            assert page.evaluate(
                """
                () => {
                    const drawer = document.querySelector(
                        '.pylage-drawer'
                    );

                    return !!(
                        drawer &&
                        !drawer.classList.contains("open")
                    );
                }
                """
            )

            # Chart must still exist in the document.
            expect(chart_locator).to_be_attached()

            # Open the drawer through the normal State pipeline.
            drawer_open.set(True)

            expect(
                drawer_locator
            ).to_be_visible(timeout=10000)

            # Chart must become usable without page reload.
            expect(
                chart_locator.locator(".plot-container")
            ).to_be_attached(timeout=15000)

            expect(
                chart_locator.locator(
                    ".plot-container svg.main-svg"
                ).first
            ).to_be_attached(timeout=15000)

            result = page.evaluate(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );

                    return {
                        hasPlotlyData: !!(
                            el &&
                            el.data &&
                            el.data.length === 1
                        ),
                        hasFullLayout: !!(
                            el &&
                            el._fullLayout
                        ),
                        width: el && el._fullLayout
                            ? el._fullLayout.width
                            : 0,
                        height: el && el._fullLayout
                            ? el._fullLayout.height
                            : 0,
                    };
                }
                """
            )

            assert result["hasPlotlyData"] is True
            assert result["hasFullLayout"] is True
            assert result["width"] > 0
            assert result["height"] > 0

            browser.close()

    finally:
        runtime.stop()

def test_chart_lifecycle_dom_replacement_and_cleanup():
    chart = Chart(
        go.Figure(
            data=[go.Bar(x=["A", "B"], y=[1, 2])]
        ),
        height=300,
    )

    runtime = Runtime(
        Column(chart),
        title="PyLage Chart DOM Replacement Test",
        output="test_output/chart_lifecycle/dom_replacement.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded")

            selector = f'[data-pylage-id="{chart.id}"]'

            page.wait_for_function(
                """
                (selector) => {
                    const el = document.querySelector(selector);
                    return !!(
                        el &&
                        el.isConnected &&
                        el._fullLayout &&
                        el.data &&
                        el.__pylageChartResizeObserver &&
                        el.__pylageChartEventsBound
                    );
                }
                """,
                arg=selector,
                timeout=15000,
            )

            page.evaluate(
                """
                (selector) => {
                    const oldEl = document.querySelector(selector);

                    if (!oldEl) {
                        throw new Error("Original chart not found");
                    }

                    const replacement = oldEl.cloneNode(false);

                    // Keep the complete PyLage chart identity and payload.
                    // Replacing the DOM node must still allow the observer
                    // to mount the replacement as a new chart instance.
                    oldEl.replaceWith(replacement);
                }
                """,
                arg=selector,
            )

            page.wait_for_function(
                """
                (selector) => {
                    const el = document.querySelector(selector);

                    return !!(
                        el &&
                        el.isConnected &&
                        el._fullLayout &&
                        el.data &&
                        el.__pylageChartResizeObserver &&
                        el.__pylageChartEventsBound
                    );
                }
                """,
                arg=selector,
                timeout=15000,
            )

            result = page.evaluate(
                """
                (selector) => {
                    const el = document.querySelector(selector);

                    return {
                        connected: !!el.isConnected,
                        hasData: !!(el.data && el.data.length),
                        hasFullLayout: !!el._fullLayout,
                        eventsBound: !!el.__pylageChartEventsBound,
                        resizeObserver: !!el.__pylageChartResizeObserver,
                    };
                }
                """,
                arg=selector,
            )

            assert result["connected"] is True
            assert result["hasData"] is True
            assert result["hasFullLayout"] is True
            assert result["eventsBound"] is True
            assert result["resizeObserver"] is True

            browser.close()

    finally:
        runtime.stop()


def test_chart_lifecycle_remove_purges_instance_and_resources():
    chart = Chart(
        go.Figure(
            data=[go.Bar(x=["A", "B"], y=[1, 2])]
        ),
        height=300,
    )

    runtime = Runtime(
        Column(chart),
        title="PyLage Chart Cleanup Test",
        output="test_output/chart_lifecycle/cleanup.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded")

            selector = f'[data-pylage-id="{chart.id}"]'

            page.wait_for_function(
                """
                (selector) => {
                    const el = document.querySelector(selector);
                    return !!(
                        el &&
                        el._fullLayout &&
                        el.data &&
                        el.__pylageChartResizeObserver &&
                        el.__pylageChartEventsBound
                    );
                }
                """,
                arg=selector,
                timeout=15000,
            )

            result = page.evaluate(
                """
                (selector) => {
                    const el = document.querySelector(selector);

                    if (!el) {
                        throw new Error("Chart not found");
                    }

                    const id = el.getAttribute("data-pylage-id");

                    window.PyLage.charts.destroy(el);

                    return {
                        id,
                        connected: el.isConnected,
                        hasData: !!(el.data && el.data.length),
                        hasFullLayout: !!el._fullLayout,
                        resizeObserver: !!el.__pylageChartResizeObserver,
                        eventsBound: !!el.__pylageChartEventsBound,
                    };
                }
                """,
                arg=selector,
            )

            assert result["connected"] is True
            assert result["hasData"] is False
            assert result["hasFullLayout"] is False
            assert result["resizeObserver"] is False
            assert result["eventsBound"] is False

            registry_state = page.evaluate(
                """
                () => ({
                    instances: window.PyLage.charts._instances
                        ? window.PyLage.charts._instances.size
                        : null
                })
                """
            )

            # The runtime intentionally does not expose its internal Map.
            # Verify the destroyed DOM element is no longer Plotly-backed.
            assert registry_state["instances"] is None

            browser.close()

    finally:
        runtime.stop()


def test_chart_lifecycle_remove_reinsert_remounts_cleanly():
    chart = Chart(
        go.Figure(
            data=[go.Bar(x=["A", "B"], y=[3, 4])]
        ),
        height=300,
    )

    runtime = Runtime(
        Column(chart),
        title="PyLage Chart Remount Test",
        output="test_output/chart_lifecycle/remount.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded")

            selector = f'[data-pylage-id="{chart.id}"]'

            page.wait_for_function(
                """
                (selector) => {
                    const el = document.querySelector(selector);
                    return !!(
                        el &&
                        el._fullLayout &&
                        el.data &&
                        el.__pylageChartResizeObserver &&
                        el.__pylageChartEventsBound
                    );
                }
                """,
                arg=selector,
                timeout=15000,
            )

            page.evaluate(
                """
                (selector) => {
                    const el = document.querySelector(selector);

                    if (!el) {
                        throw new Error("Chart not found");
                    }

                    window.__pylageRemovedChartHTML = el.outerHTML;
                    el.remove();
                }
                """,
                arg=selector,
            )

            page.wait_for_function(
                """
                () => !document.querySelector(
                    '[data-pylage-chart="1"]'
                )
                """,
                timeout=10000,
            )

            # Reinsert the exact same chart markup. MutationObserver must
            # treat it as a fresh mount after the previous instance was
            # destroyed.
            page.evaluate(
                """
                (selector) => {
                    const html = window.__pylageRemovedChartHTML;

                    if (!html) {
                        throw new Error(
                            "Removed chart snapshot is missing"
                        );
                    }

                    const wrapper = document.createElement("div");
                    wrapper.innerHTML = html;

                    document.body.appendChild(
                        wrapper.firstElementChild
                    );
                }
                """,
                arg=selector,
            )

            page.wait_for_function(
                """
                (selector) => {
                    const el = document.querySelector(selector);

                    return !!(
                        el &&
                        el._fullLayout &&
                        el.data &&
                        el.__pylageChartResizeObserver &&
                        el.__pylageChartEventsBound
                    );
                }
                """,
                arg=selector,
                timeout=15000,
            )

            result = page.evaluate(
                """
                (selector) => {
                    const el = document.querySelector(selector);

                    return {
                        connected: !!el.isConnected,
                        hasData: !!(el.data && el.data.length),
                        hasFullLayout: !!el._fullLayout,
                        eventsBound: !!el.__pylageChartEventsBound,
                        resizeObserver: !!el.__pylageChartResizeObserver,
                    };
                }
                """,
                arg=selector,
            )

            assert result["connected"] is True
            assert result["hasData"] is True
            assert result["hasFullLayout"] is True
            assert result["eventsBound"] is True
            assert result["resizeObserver"] is True

            browser.close()

    finally:
        runtime.stop()


def test_chart_lifecycle_repeated_remove_reinsert_does_not_duplicate_charts():
    chart = Chart(
        go.Figure(
            data=[go.Bar(x=["A", "B"], y=[5, 6])]
        ),
        height=300,
    )

    runtime = Runtime(
        Column(chart),
        title="PyLage Chart Lifecycle Repeat Test",
        output="test_output/chart_lifecycle/repeat.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded")

            selector = f'[data-pylage-id="{chart.id}"]'

            page.wait_for_function(
                """
                (selector) => {
                    const el = document.querySelector(selector);
                    return !!(
                        el &&
                        el._fullLayout &&
                        el.data &&
                        el.__pylageChartResizeObserver
                    );
                }
                """,
                arg=selector,
                timeout=15000,
            )

            for _ in range(50):
                page.evaluate(
                    """
                    (selector) => {
                        const el = document.querySelector(selector);

                        if (!el) {
                            throw new Error("Chart not found");
                        }

                        const html = el.outerHTML;
                        el.remove();

                        const wrapper = document.createElement("div");
                        wrapper.innerHTML = html;

                        const replacement = wrapper.firstElementChild;

                        document.body.appendChild(replacement);
                    }
                    """,
                    arg=selector,
                )

                page.wait_for_function(
                    """
                    () => {
                        const charts = document.querySelectorAll(
                            '[data-pylage-chart="1"]'
                        );

                        return charts.length === 1 &&
                            !!charts[0]._fullLayout &&
                            !!charts[0].data;
                    }
                    """,
                    timeout=15000,
                )

            final_state = page.evaluate(
                """
                () => {
                    const charts = Array.from(
                        document.querySelectorAll(
                            '[data-pylage-chart="1"]'
                        )
                    );

                    return {
                        count: charts.length,
                        allMounted: charts.every(
                            el =>
                                !!el._fullLayout &&
                                !!el.data &&
                                !!el.__pylageChartResizeObserver
                        ),
                    };
                }
                """
            )

            assert final_state["count"] == 1
            assert final_state["allMounted"] is True

            browser.close()

    finally:
        runtime.stop()

def test_chart_lifecycle_navigation_replaces_chart_cleanly(tmp_path):
    from pylage.ENGINE.routing import Router
    from pylage.ENGINE.routing.runtime import RoutingRuntime

    pages = tmp_path / "pages"
    pages.mkdir()

    (pages / "first.py").write_text(
        """
import plotly.graph_objects as go
import pylage as pl

def page():
    return pl.Chart(
        go.Figure(
            data=[go.Bar(x=["A", "B"], y=[1, 2])]
        ),
        height=300,
        title="First Chart",
    )
""",
        encoding="utf-8",
    )

    (pages / "second.py").write_text(
        """
import plotly.graph_objects as go
import pylage as pl

def page():
    return pl.Chart(
        go.Figure(
            data=[go.Bar(x=["X", "Y"], y=[3, 4])]
        ),
        height=300,
        title="Second Chart",
    )
""",
        encoding="utf-8",
    )

    root = Column()
    routing = RoutingRuntime(Router(pages), root)

    runtime = Runtime(
        root,
        title="PyLage Chart Navigation Lifecycle Test",
        output="test_output/chart_lifecycle/navigation.html",
        navigation_handler=routing.navigate,
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            # Navigate to the first route through the browser runtime.
            page.evaluate(
                """
                () => {
                    if (!window.PyLage || !window.PyLage.navigate) {
                        throw new Error(
                            "PyLage navigation runtime is unavailable"
                        );
                    }

                    window.PyLage.navigate("/first");
                }
                """
            )

            selector = '[data-pylage-chart="1"]'

            page.wait_for_function(
                """
                (selector) => {
                    const charts =
                        document.querySelectorAll(selector);

                    return charts.length === 1 &&
                        !!charts[0]._fullLayout &&
                        !!charts[0].data &&
                        !!charts[0].__pylageChartResizeObserver;
                }
                """,
                arg=selector,
                timeout=15000,
            )

            first_state = page.evaluate(
                """
                () => {
                    const chart =
                        document.querySelector(
                            '[data-pylage-chart="1"]'
                        );

                    return {
                        count:
                            document.querySelectorAll(
                                '[data-pylage-chart="1"]'
                            ).length,
                        title:
                            chart &&
                            chart.getAttribute("aria-label"),
                        mounted:
                            !!(
                                chart &&
                                chart._fullLayout &&
                                chart.data
                            ),
                    };
                }
                """
            )

            assert first_state["count"] == 1
            assert first_state["mounted"] is True
            assert first_state["title"] == "First Chart"

            # Route transition replaces the root child. The old chart must
            # be destroyed and the new chart must mount exactly once.
            page.evaluate(
                """
                () => {
                    window.PyLage.navigate("/second");
                }
                """
            )

            page.wait_for_function(
                """
                (selector) => {
                    const charts =
                        document.querySelectorAll(selector);

                    if (charts.length !== 1) {
                        return false;
                    }

                    const chart = charts[0];

                    return !!(
                        chart._fullLayout &&
                        chart.data &&
                        chart.__pylageChartResizeObserver &&
                        chart.__pylageChartEventsBound
                    );
                }
                """,
                arg=selector,
                timeout=15000,
            )

            second_state = page.evaluate(
                """
                () => {
                    const charts = Array.from(
                        document.querySelectorAll(
                            '[data-pylage-chart="1"]'
                        )
                    );

                    return {
                        count: charts.length,
                        title:
                            charts[0] &&
                            charts[0].getAttribute("aria-label"),
                        mounted: !!(
                            charts[0] &&
                            charts[0]._fullLayout &&
                            charts[0].data
                        ),
                        x:
                            charts[0] &&
                            charts[0].data &&
                            charts[0].data[0] &&
                            charts[0].data[0].x
                                ? Array.from(charts[0].data[0].x)
                                : [],
                    };
                }
                """
            )

            assert second_state["count"] == 1
            assert second_state["mounted"] is True
            assert second_state["title"] == "Second Chart"
            assert second_state["x"] == ["X", "Y"]

            browser.close()

    finally:
        runtime.stop()

def test_chart_lifecycle_runtime_reload_remounts_chart():
    from pylage.ENGINE import Heading

    old_chart = Chart(
        go.Figure(
            data=[go.Bar(x=["A", "B"], y=[1, 2])]
        ),
        height=300,
        title="Old Reload Chart",
    )

    new_chart = Chart(
        go.Figure(
            data=[go.Bar(x=["X", "Y"], y=[7, 8])]
        ),
        height=300,
        title="New Reload Chart",
    )

    old_app = Column(old_chart)
    new_app = Column(new_chart)

    runtime = Runtime(
        old_app,
        title="PyLage Chart Runtime Reload Test",
        output="test_output/chart_lifecycle/runtime_reload.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            selector = '[data-pylage-chart="1"]'

            page.wait_for_function(
                """
                (selector) => {
                    const charts =
                        document.querySelectorAll(selector);

                    return charts.length === 1 &&
                        !!charts[0]._fullLayout &&
                        !!charts[0].data &&
                        !!charts[0].__pylageChartResizeObserver &&
                        !!charts[0].__pylageChartEventsBound;
                }
                """,
                arg=selector,
                timeout=15000,
            )

            old_state = page.evaluate(
                """
                () => {
                    const chart =
                        document.querySelector(
                            '[data-pylage-chart="1"]'
                        );

                    return {
                        title:
                            chart &&
                            chart.getAttribute("aria-label"),
                        x:
                            chart &&
                            chart.data &&
                            chart.data[0] &&
                            chart.data[0].x
                                ? Array.from(chart.data[0].x)
                                : [],
                        mounted: !!(
                            chart &&
                            chart._fullLayout &&
                            chart.data
                        ),
                    };
                }
                """
            )

            assert old_state["title"] == "Old Reload Chart"
            assert old_state["x"] == ["A", "B"]
            assert old_state["mounted"] is True

            # Runtime reload sends the reload message over the active
            # WebSocket. The browser handles it with location.reload().
            runtime.reload_app(new_app)

            page.wait_for_function(
                """
                (selector) => {
                    const charts =
                        document.querySelectorAll(selector);

                    if (charts.length !== 1) {
                        return false;
                    }

                    const chart = charts[0];

                    return (
                        chart.getAttribute("aria-label") ===
                            "New Reload Chart" &&
                        !!chart._fullLayout &&
                        !!chart.data &&
                        !!chart.__pylageChartResizeObserver &&
                        !!chart.__pylageChartEventsBound
                    );
                }
                """,
                arg=selector,
                timeout=20000,
            )

            new_state = page.evaluate(
                """
                () => {
                    const charts = Array.from(
                        document.querySelectorAll(
                            '[data-pylage-chart="1"]'
                        )
                    );

                    return {
                        count: charts.length,
                        title:
                            charts[0] &&
                            charts[0].getAttribute("aria-label"),
                        x:
                            charts[0] &&
                            charts[0].data &&
                            charts[0].data[0] &&
                            charts[0].data[0].x
                                ? Array.from(charts[0].data[0].x)
                                : [],
                        mounted: !!(
                            charts[0] &&
                            charts[0]._fullLayout &&
                            charts[0].data
                        ),
                        resizeObserver: !!(
                            charts[0] &&
                            charts[0].__pylageChartResizeObserver
                        ),
                        eventsBound: !!(
                            charts[0] &&
                            charts[0].__pylageChartEventsBound
                        ),
                    };
                }
                """
            )

            assert new_state["count"] == 1
            assert new_state["title"] == "New Reload Chart"
            assert new_state["x"] == ["X", "Y"]
            assert new_state["mounted"] is True
            assert new_state["resizeObserver"] is True
            assert new_state["eventsBound"] is True

            browser.close()

    finally:
        runtime.stop()



def test_chart_lifecycle_websocket_reconnect_remounts_cleanly():
    chart = Chart(
        go.Figure(
            data=[
                go.Bar(
                    x=["A", "B"],
                    y=[10, 20],
                    name="Reconnect",
                )
            ],
            layout={"title": {"text": "Reconnect Chart"}},
        ),
        title="Reconnect Chart",
    )

    runtime = Runtime(
        Column(chart),
        title="PyLage Chart WebSocket Reconnect Test",
        output="test_output/chart_lifecycle/websocket_reconnect.html",
    )

    try:
        url = runtime.start()
        websocket_server = runtime._websocket
        assert websocket_server is not None

        # Force a deterministic server restart on the same WebSocket endpoint.
        websocket_url = websocket_server.url
        websocket_port = websocket_server.port

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            chart_locator = page.locator(
                f'[data-pylage-id="{chart.id}"]'
            )

            expect(chart_locator.locator(".plot-container")).to_be_attached(
                timeout=10000
            )

            initial_state = page.evaluate(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );

                    return {
                        socketOpen: !!(
                            window.PyLage &&
                            window.PyLage.socket &&
                            window.PyLage.socket.readyState === WebSocket.OPEN
                        ),
                        chartCount: document.querySelectorAll(
                            '[data-pylage-chart="1"]'
                        ).length,
                        x: el && el.data && el.data[0]
                            ? el.data[0].x
                            : null,
                        hasFullLayout: !!(el && el._fullLayout),
                        resizeObserver: !!(
                            el &&
                            el.__pylageChartResizeObserver
                        ),
                        eventsBound: !!(
                            el &&
                            el.__pylageChartEventsBound
                        ),
                    };
                }
                """
            )

            assert initial_state == {
                "socketOpen": True,
                "chartCount": 1,
                "x": ["A", "B"],
                "hasFullLayout": True,
                "resizeObserver": True,
                "eventsBound": True,
            }

            # Stop only the WebSocket transport. Keep the Runtime and
            # generated document alive so the browser can exercise its
            # automatic reconnect path.
            websocket_server.stop()

            page.wait_for_function(
                """
                () => !(
                    window.PyLage &&
                    window.PyLage.socket &&
                    window.PyLage.socket.readyState === WebSocket.OPEN
                )
                """,
                timeout=10000,
            )

            # Restart the same server on the same port so the browser's
            # existing reconnect URL becomes available again.
            assert websocket_server.port == websocket_port
            assert websocket_server.start() == websocket_url

            # The client starts reconnecting after its backoff delay.
            page.wait_for_function(
                """
                () => !!(
                    window.PyLage &&
                    window.PyLage.socket &&
                    window.PyLage.socket.readyState === WebSocket.OPEN
                )
                """,
                timeout=15000,
            )

            page.wait_for_function(
                """
                () => {
                    const charts = document.querySelectorAll(
                        '[data-pylage-chart="1"]'
                    );

                    const el = charts.length === 1 ? charts[0] : null;

                    return !!(
                        el &&
                        el.data &&
                        el.data[0] &&
                        el.data[0].x &&
                        el.data[0].x.length === 2 &&
                        el.data[0].x[0] === "A" &&
                        el.data[0].x[1] === "B" &&
                        el._fullLayout &&
                        el.__pylageChartResizeObserver &&
                        el.__pylageChartEventsBound
                    );
                }
                """,
                timeout=10000,
            )

            reconnected_state = page.evaluate(
                """
                () => {
                    const charts = document.querySelectorAll(
                        '[data-pylage-chart="1"]'
                    );
                    const el = charts.length === 1 ? charts[0] : null;

                    return {
                        socketOpen: !!(
                            window.PyLage &&
                            window.PyLage.socket &&
                            window.PyLage.socket.readyState === WebSocket.OPEN
                        ),
                        chartCount: charts.length,
                        x: el && el.data && el.data[0]
                            ? el.data[0].x
                            : null,
                        hasFullLayout: !!(el && el._fullLayout),
                        resizeObserver: !!(
                            el &&
                            el.__pylageChartResizeObserver
                        ),
                        eventsBound: !!(
                            el &&
                            el.__pylageChartEventsBound
                        ),
                    };
                }
                """
            )

            assert reconnected_state == {
                "socketOpen": True,
                "chartCount": 1,
                "x": ["A", "B"],
                "hasFullLayout": True,
                "resizeObserver": True,
                "eventsBound": True,
            }

            browser.close()
    finally:
        runtime.stop()




def test_chart_plotly_events_dispatch_click_select_relayout_and_hover():
    calls = []

    def on_click(payload):
        calls.append(("click", payload))

    def on_select(payload):
        calls.append(("select", payload))

    def on_relayout(payload):
        calls.append(("relayout", payload))

    def on_hover(payload):
        calls.append(("hover", payload))

    chart = Chart(
        go.Figure(
            data=[
                go.Scatter(
                    x=[1, 2, 3],
                    y=[10, 20, 30],
                    mode="markers",
                )
            ]
        ),
        title="Chart Event Test",
        on_click=on_click,
        on_select=on_select,
        on_relayout=on_relayout,
        on_hover=on_hover,
    )

    app = Column(chart)

    runtime = Runtime(
        app,
        title="PyLage Chart Event Browser Test",
        output="test_output/chart_browser/events.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url)
            page.wait_for_function(
                """() => {
                    const el = document.querySelector('[data-pylage-chart="1"]');
                    return el && el.__pylageChartEventsBound;
                }"""
            )

            page.evaluate(
                """() => {
                    const el = document.querySelector('[data-pylage-chart="1"]');

                    el.emit("plotly_click", {
                        points: [{
                            curveNumber: 0,
                            pointNumber: 1,
                            pointIndex: 1,
                            x: 2,
                            y: 20,
                            text: "B",
                            label: "B"
                        }]
                    });

                    el.emit("plotly_selected", {
                        points: [{
                            curveNumber: 0,
                            pointNumber: 0,
                            pointIndex: 0,
                            x: 1,
                            y: 10,
                            text: "A",
                            label: "A"
                        }],
                        range: {
                            x: [1, 2],
                            y: [10, 20]
                        }
                    });

                    el.emit("plotly_relayout", {
                        "xaxis.range[0]": 1,
                        "xaxis.range[1]": 3
                    });

                    el.emit("plotly_hover", {
                        points: [{
                            curveNumber: 0,
                            pointNumber: 2,
                            pointIndex: 2,
                            x: 3,
                            y: 30,
                            text: "C",
                            label: "C"
                        }]
                    });
                }"""
            )

            page.wait_for_timeout(500)

            browser.close()
    finally:
        runtime.stop()

    assert any(name == "click" for name, _ in calls)
    assert any(name == "select" for name, _ in calls)
    assert any(name == "relayout" for name, _ in calls)
    assert any(name == "hover" for name, _ in calls)

def test_chart_initial_conversion_failure_uses_error_fallback():
    chart = Chart(object())

    payload = chart.props["_chart_payload"].value
    assert '"backend":"none"' in payload
    assert '"Chart error"' in payload
    assert '"data":[]' in payload


def test_chart_config_javascript_string_is_not_executed():
    chart = Chart(
        go.Figure(data=[go.Bar(x=["A"], y=[1])]),
        config={
            "customScript": "<script>window.__pylage_config_xss=1</script>",
            "customHandler": "javascript:window.__pylage_config_xss=1",
        },
    )

    app = Column(chart)

    runtime = Runtime(
        app,
        title="PyLage Chart Config Security Test",
        output="test_output/chart_browser/config_security.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            result = page.evaluate(
                """
                () => ({
                    executed: window.__pylage_config_xss === 1,
                    scripts: document.scripts.length,
                    payload: document.querySelector(
                        '[data-pylage-chart="1"]'
                    )?.getAttribute("data-chart-payload") || "",
                })
                """
            )

            assert result["executed"] is False
            assert "<script>" in result["payload"]
            assert "javascript:" in result["payload"]

            browser.close()
    finally:
        runtime.stop()
