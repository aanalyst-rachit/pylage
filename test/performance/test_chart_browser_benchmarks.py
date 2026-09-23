from time import perf_counter

import plotly.graph_objects as go
from playwright.sync_api import sync_playwright

from pylage.ENGINE import Column, State
from pylage import Chart
from pylage.ENGINE.runtime import Runtime


def _figure(x_values, y_values, name="benchmark"):
    return go.Figure(
        data=[
            go.Scatter(
                x=x_values,
                y=y_values,
                mode="lines+markers",
                name=name,
            )
        ]
    )


def _build_runtime():
    chart_state = State(
        _figure(
            list(range(100)),
            list(range(100)),
        )
    )

    chart = Chart(
        chart_state,
        height=350,
        title="Phase 12 Browser Benchmark",
    )

    runtime = Runtime(
        Column(chart),
        title="Phase 12 Browser Benchmark",
        output="test_output/chart_browser/benchmark.html",
    )

    return chart_state, runtime


def test_phase12_browser_initialization_benchmark():
    chart_state, runtime = _build_runtime()

    try:
        start = perf_counter()

        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            browser.close()

        elapsed = perf_counter() - start

        assert url
        assert elapsed >= 0

        print()
        print("===== PHASE 12 — BROWSER INITIALIZATION =====")
        print(f"total             : {elapsed:.9f}s")

    finally:
        runtime.stop()


def test_phase12_initial_chart_render_benchmark():
    chart_state, runtime = _build_runtime()

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            start = perf_counter()

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
                        el.data &&
                        window.Plotly
                    );
                }
                """,
                timeout=10000,
            )

            elapsed = perf_counter() - start

            assert page.locator(
                '[data-pylage-chart="1"]'
            ).count() == 1

            print()
            print("===== PHASE 12 — INITIAL CHART RENDER =====")
            print(f"total             : {elapsed:.9f}s")

            browser.close()

    finally:
        runtime.stop()


def test_phase12_reactive_chart_update_benchmark():
    chart_state, runtime = _build_runtime()

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

            start = perf_counter()

            chart_state.set(
                _figure(
                    list(range(120)),
                    list(range(120)),
                    name="updated",
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
                        el.data[0].x.length === 120
                    );
                }
                """,
                timeout=10000,
            )

            elapsed = perf_counter() - start

            assert page.evaluate(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );
                    return el.data[0].x.length === 120;
                }
                """
            )

            print()
            print("===== PHASE 12 — REACTIVE UPDATE =====")
            print(f"total             : {elapsed:.9f}s")

            browser.close()

    finally:
        runtime.stop()


def test_phase12_repeated_reactive_updates_benchmark():
    chart_state, runtime = _build_runtime()

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

            update_count = 20

            start = perf_counter()

            for update in range(update_count):
                chart_state.set(
                    _figure(
                        list(range(100 + update)),
                        list(range(100 + update)),
                        name=f"update-{update}",
                    )
                )

                expected_length = 100 + update

                page.wait_for_function(
                    """
                    expected => {
                        const el = document.querySelector(
                            '[data-pylage-chart="1"]'
                        );

                        return !!(
                            el &&
                            el.data &&
                            el.data[0] &&
                            el.data[0].x &&
                            el.data[0].x.length === expected
                        );
                    }
                    """,
                    arg=expected_length,
                    timeout=10000,
                )

            elapsed = perf_counter() - start

            final_length = page.evaluate(
                """
                () => {
                    const el = document.querySelector(
                        '[data-pylage-chart="1"]'
                    );

                    return el.data[0].x.length;
                }
                """
            )

            assert final_length == 119

            print()
            print("===== PHASE 12 — REPEATED REACTIVE UPDATES =====")
            print(f"updates            : {update_count}")
            print(f"total              : {elapsed:.9f}s")
            print(f"per update         : {elapsed / update_count:.9f}s")

            browser.close()

    finally:
        runtime.stop()


def test_phase12_multiple_charts_page_benchmark():
    states = []
    charts = []

    for index in range(10):
        state = State(
            _figure(
                list(range(50)),
                list(range(50)),
                name=f"chart-{index}",
            )
        )
        states.append(state)
        charts.append(
            Chart(
                state,
                height=300,
                title=f"Chart {index}",
            )
        )

    runtime = Runtime(
        Column(*charts),
        title="Phase 12 Multiple Charts Benchmark",
        output="test_output/chart_browser/multiple.html",
    )

    try:
        start = perf_counter()
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            page.wait_for_function(
                """
                () => {
                    const charts = document.querySelectorAll(
                        '[data-pylage-chart="1"]'
                    );

                    return charts.length === 10 &&
                        Array.from(charts).every(
                            el => el._fullLayout && el.data
                        );
                }
                """,
                timeout=15000,
            )

            elapsed = perf_counter() - start

            chart_count = page.locator(
                '[data-pylage-chart="1"]'
            ).count()

            assert chart_count == 10

            print()
            print("===== PHASE 12 — MULTIPLE CHARTS PAGE =====")
            print("charts             : 10")
            print(f"total              : {elapsed:.9f}s")
            print(f"per chart          : {elapsed / 10:.9f}s")

            browser.close()

    finally:
        runtime.stop()


def test_phase12_plotly_asset_loading_and_cache_benchmark():
    chart_state, runtime = _build_runtime()
    runtime.start()

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()

            try:
                first_page = context.new_page()
                first_requests = []

                first_page.on(
                    "request",
                    lambda request: (
                        first_requests.append(request.url)
                        if "plotly.min.js" in request.url.lower()
                        else None
                    ),
                )

                start = perf_counter()
                first_page.goto(
                    runtime.url,
                    wait_until="domcontentloaded",
                )
                first_page.wait_for_function(
                    "() => window.Plotly !== undefined"
                )
                first_page.wait_for_function(
                    "() => document.querySelector('[data-pylage-chart]') !== null"
                )
                first_load = perf_counter() - start

                assert first_requests

                plotly_url = first_requests[0]

                first_entry = first_page.evaluate(
                    """
                    (url) => {
                        const entries = performance
                            .getEntriesByType("resource")
                            .filter(entry => entry.name === url);

                        return entries.length
                            ? entries[entries.length - 1].toJSON()
                            : null;
                    }
                    """,
                    plotly_url,
                )

                first_page.close()

                second_page = context.new_page()
                second_requests = []

                second_page.on(
                    "request",
                    lambda request: (
                        second_requests.append(request.url)
                        if "plotly.min.js" in request.url.lower()
                        else None
                    ),
                )

                start = perf_counter()
                second_page.goto(
                    runtime.url,
                    wait_until="domcontentloaded",
                )
                second_page.wait_for_function(
                    "() => window.Plotly !== undefined"
                )
                second_page.wait_for_function(
                    "() => document.querySelector('[data-pylage-chart]') !== null"
                )
                second_load = perf_counter() - start

                second_entry = second_page.evaluate(
                    """
                    (url) => {
                        const entries = performance
                            .getEntriesByType("resource")
                            .filter(entry => entry.name === url);

                        return entries.length
                            ? entries[entries.length - 1].toJSON()
                            : null;
                    }
                    """,
                    plotly_url,
                )

                print()
                print("===== PHASE 12 — PLOTLY.JS CACHE EVIDENCE =====")
                print(f"asset URL            : {plotly_url}")
                print(f"first requests       : {len(first_requests)}")
                print(f"second requests      : {len(second_requests)}")
                print(f"first load time      : {first_load:.9f}s")
                print(f"second load time     : {second_load:.9f}s")
                print(
                    f"first transfer size  : "
                    f"{first_entry.get('transferSize') if first_entry else None}"
                )
                print(
                    f"second transfer size : "
                    f"{second_entry.get('transferSize') if second_entry else None}"
                )
                print(
                    f"first encoded bytes  : "
                    f"{first_entry.get('encodedBodySize') if first_entry else None}"
                )
                print(
                    f"second encoded bytes : "
                    f"{second_entry.get('encodedBodySize') if second_entry else None}"
                )

                assert first_entry is not None
                assert second_entry is not None
                assert len(first_requests) == 1
                assert len(second_requests) <= 1

            finally:
                context.close()
                browser.close()
    finally:
        runtime.stop()
