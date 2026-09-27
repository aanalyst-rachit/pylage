from playwright.sync_api import expect, sync_playwright

from pylage.ENGINE import Button, Column, Drawer, State, Text
from pylage.ENGINE.runtime import Runtime


def test_drawer_focuses_first_focusable_child_when_opened():
    open_state = State(False)
    drawer = Drawer(
        Column(
            Text("Drawer content"),
            Button("First action"),
            Button("Second action"),
        ),
        open=open_state,
    )
    trigger = Button("Open drawer")
    app = Column(trigger, drawer)

    runtime = Runtime(
        app,
        title="PyLage Drawer Focus Entry Browser Test",
        output="test_output/drawer_browser/focus_entry.html",
    )

    try:
        url = runtime.start()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_function(
                    "() => window.PyLage && window.PyLage.socket && window.PyLage.socket.readyState === WebSocket.OPEN",
                    timeout=10000,
                )

                trigger_locator = page.locator(
                    f'button[data-pylage-id="{trigger.id}"]'
                )
                drawer_locator = page.locator(
                    f'aside[data-pylage-id="{drawer.id}"]'
                )
                first_action = drawer_locator.locator("button").first

                trigger_locator.focus()
                expect(trigger_locator).to_be_focused()

                open_state.set(True)

                expect(drawer_locator).to_have_attribute(
                    "open",
                    "",
                    timeout=10000,
                )
                expect(drawer_locator).to_have_attribute(
                    "aria-hidden",
                    "false",
                )
                expect(first_action).to_be_focused(timeout=10000)
            finally:
                browser.close()
    finally:
        runtime.stop()


def test_drawer_restores_focus_to_trigger_when_closed():
    open_state = State(False)
    drawer = Drawer(
        Column(
            Text("Drawer content"),
            Button("First action"),
        ),
        open=open_state,
    )
    trigger = Button("Open drawer")
    app = Column(trigger, drawer)

    def dismiss():
        open_state.set(False)

    drawer.events["dismiss"] = dismiss

    runtime = Runtime(
        app,
        title="PyLage Drawer Focus Restoration Browser Test",
        output="test_output/drawer_browser/focus_restoration.html",
    )

    try:
        url = runtime.start()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_function(
                    "() => window.PyLage && window.PyLage.socket && window.PyLage.socket.readyState === WebSocket.OPEN",
                    timeout=10000,
                )

                trigger_locator = page.locator(
                    f'button[data-pylage-id="{trigger.id}"]'
                )
                drawer_locator = page.locator(
                    f'aside[data-pylage-id="{drawer.id}"]'
                )
                first_action = drawer_locator.locator("button").first

                trigger_locator.focus()
                expect(trigger_locator).to_be_focused()

                open_state.set(True)

                expect(drawer_locator).to_have_attribute(
                    "open",
                    "",
                    timeout=10000,
                )
                expect(first_action).to_be_focused(timeout=10000)

                open_state.set(False)

                expect(drawer_locator).not_to_have_attribute(
                    "open",
                    timeout=10000,
                )
                expect(drawer_locator).to_have_attribute(
                    "aria-hidden",
                    "true",
                )
                expect(trigger_locator).to_be_focused(timeout=10000)
            finally:
                browser.close()
    finally:
        runtime.stop()








def test_drawer_focuses_itself_when_opened_without_focusable_children():
    open_state = State(False)
    drawer = Drawer(Text("Drawer content"), open=open_state)
    trigger = Button("Open drawer")
    app = Column(trigger, drawer)

    runtime = Runtime(
        app,
        title="PyLage Drawer Focus Fallback Browser Test",
        output="test_output/drawer_browser/focus_fallback.html",
    )

    try:
        url = runtime.start()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_function(
                    "() => window.PyLage && window.PyLage.socket && window.PyLage.socket.readyState === WebSocket.OPEN",
                    timeout=10000,
                )

                trigger_locator = page.locator(
                    f'button[data-pylage-id="{trigger.id}"]'
                )
                drawer_locator = page.locator(
                    f'aside[data-pylage-id="{drawer.id}"]'
                )

                trigger_locator.focus()
                open_state.set(True)

                expect(drawer_locator).to_have_attribute(
                    "open",
                    "",
                    timeout=10000,
                )
                expect(drawer_locator).to_have_attribute(
                    "tabindex",
                    "-1",
                    timeout=10000,
                )
                expect(drawer_locator).to_be_focused(timeout=10000)
            finally:
                browser.close()
    finally:
        runtime.stop()


def test_drawer_backdrop_click_dismisses_drawer_in_browser():
    open_state = State(False)

    def dismiss():
        open_state.set(False)

    drawer = Drawer(
        Text("Drawer content"),
        open=open_state,
        on_dismiss=dismiss,
    )

    app = Column(drawer)

    runtime = Runtime(
        app,
        title="PyLage Drawer Dismiss Browser Test",
        output="test_output/drawer_browser/dismiss.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            page.wait_for_function(
                """
                () => (
                    window.PyLage &&
                    window.PyLage.socket &&
                    window.PyLage.socket.readyState === WebSocket.OPEN
                )
                """,
                timeout=10000,
            )

            drawer_locator = page.locator(
                f'aside[data-pylage-id="{drawer.id}"]'
            )
            backdrop = page.locator(
                ".pylage-drawer-backdrop"
            )

            expect(drawer_locator).not_to_have_attribute(
                "open"
            )

            open_state.set(True)

            expect(drawer_locator).to_have_attribute(
                "open",
                "",
                timeout=10000,
            )

            expect(backdrop).to_be_visible()

            backdrop.click()

            expect(drawer_locator).not_to_have_attribute(
                "open",
                timeout=10000,
            )

            browser.close()

    finally:
        runtime.stop()


def test_drawer_all_positions_have_correct_viewport_geometry():
    states = {
        position: State(False)
        for position in ("left", "right", "top", "bottom")
    }

    drawers = {
        position: Drawer(
            Text(f"{position} drawer"),
            open=state,
            position=position,
        )
        for position, state in states.items()
    }

    app = Column(*drawers.values())

    runtime = Runtime(
        app,
        title="PyLage Drawer Direction Browser Test",
        output="test_output/drawer_browser/directions.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 800})

            try:
                page.goto(url, wait_until="domcontentloaded")

                page.wait_for_function(
                    "() => window.PyLage && window.PyLage.socket && window.PyLage.socket.readyState === WebSocket.OPEN",
                    timeout=10000,
                )

                for position, state in states.items():
                    drawer = page.locator(
                        f'aside[data-pylage-id="{drawers[position].id}"]'
                    )

                    expect(drawer).not_to_have_attribute("open")

                    state.set(True)

                    expect(drawer).to_have_attribute(
                        "open",
                        "",
                        timeout=10000,
                    )

                    expected_x = 0 if position in ("left", "top", "bottom") else 960
                    expected_y = 0 if position in ("left", "right", "top") else 480

                    page.wait_for_function(
                        "(args) => { const r = document.querySelector(args.selector)?.getBoundingClientRect(); return r && Math.abs(r.x - args.x) < 0.5 && Math.abs(r.y - args.y) < 0.5; }",
                        arg={
                            "selector": "aside[data-pylage-id=" + chr(34) + str(drawers[position].id) + chr(34) + "]",
                            "x": expected_x,
                            "y": expected_y,
                        },
                        timeout=10000,
                    )

                    box = drawer.bounding_box()
                    assert box is not None

                    if position in ("left", "right"):
                        assert box["width"] == 320
                        assert box["height"] == 800
                        assert box["y"] == 0

                        if position == "left":
                            assert box["x"] == 0
                        else:
                            assert box["x"] == 960
                    else:
                        assert box["width"] == 1280
                        assert box["height"] == 320
                        assert box["x"] == 0

                        if position == "top":
                            assert box["y"] == 0
                        else:
                            assert box["y"] == 480

                    state.set(False)

                    expect(drawer).not_to_have_attribute(
                        "open",
                        timeout=10000,
                    )

            finally:
                browser.close()

    finally:
        runtime.stop()

def test_drawer_escape_key_dismisses_open_drawer_in_browser():
    open_state = State(False)

    def dismiss():
        open_state.set(False)

    drawer = Drawer(
        Text("Drawer content"),
        open=open_state,
        on_dismiss=dismiss,
    )

    app = Column(drawer)

    runtime = Runtime(
        app,
        title="PyLage Drawer Escape Browser Test",
        output="test_output/drawer_browser/escape.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                page.goto(url, wait_until="domcontentloaded")

                page.wait_for_function(
                    """
                    () => (
                        window.PyLage &&
                        window.PyLage.socket &&
                        window.PyLage.socket.readyState === WebSocket.OPEN
                    )
                    """,
                    timeout=10000,
                )

                drawer_locator = page.locator(
                    f'aside[data-pylage-id="{drawer.id}"]'
                )

                expect(drawer_locator).not_to_have_attribute("open")

                page.keyboard.press("Escape")

                expect(drawer_locator).not_to_have_attribute("open")

                open_state.set(True)

                expect(drawer_locator).to_have_attribute(
                    "open",
                    "",
                    timeout=10000,
                )

                page.keyboard.press("Escape")

                expect(drawer_locator).not_to_have_attribute(
                    "open",
                    timeout=10000,
                )

            finally:
                browser.close()

    finally:
        runtime.stop()

def test_drawer_escape_key_dismisses_topmost_open_drawer_only():
    first_open = State(False)
    second_open = State(False)

    def dismiss_first():
        first_open.set(False)

    def dismiss_second():
        second_open.set(False)

    first = Drawer(
        Text("First drawer"),
        open=first_open,
        on_dismiss=dismiss_first,
    )
    second = Drawer(
        Text("Second drawer"),
        open=second_open,
        on_dismiss=dismiss_second,
    )

    app = Column(first, second)

    runtime = Runtime(
        app,
        title="PyLage Drawer Escape Stack Browser Test",
        output="test_output/drawer_browser/escape_stack.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                page.goto(url, wait_until="domcontentloaded")

                page.wait_for_function(
                    """
                    () => (
                        window.PyLage &&
                        window.PyLage.socket &&
                        window.PyLage.socket.readyState === WebSocket.OPEN
                    )
                    """,
                    timeout=10000,
                )

                first_locator = page.locator(
                    f'aside[data-pylage-id="{first.id}"]'
                )
                second_locator = page.locator(
                    f'aside[data-pylage-id="{second.id}"]'
                )

                first_open.set(True)
                second_open.set(True)

                expect(first_locator).to_have_attribute(
                    "open",
                    "",
                    timeout=10000,
                )
                expect(second_locator).to_have_attribute(
                    "open",
                    "",
                    timeout=10000,
                )

                page.keyboard.press("Escape")

                expect(second_locator).not_to_have_attribute(
                    "open",
                    timeout=10000,
                )
                expect(first_locator).to_have_attribute(
                    "open",
                    "",
                    timeout=10000,
                )

            finally:
                browser.close()

    finally:
        runtime.stop()


def test_persistent_drawer_does_not_steal_focus_when_opened():
    open_state = State(False)
    drawer = Drawer(
        Column(Button("Drawer action")),
        open=open_state,
        modal=False,
    )
    trigger = Button("Background action")
    app = Column(trigger, drawer)

    runtime = Runtime(
        app,
        title="PyLage Persistent Drawer Focus Browser Test",
        output="test_output/drawer_browser/persistent_focus.html",
    )

    try:
        url = runtime.start()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_function(
                    "() => window.PyLage && window.PyLage.socket && window.PyLage.socket.readyState === WebSocket.OPEN",
                    timeout=10000,
                )

                trigger_locator = page.locator(f'button[data-pylage-id="{trigger.id}"]')
                drawer_locator = page.locator(f'aside[data-pylage-id="{drawer.id}"]')

                trigger_locator.focus()
                expect(trigger_locator).to_be_focused()

                open_state.set(True)

                expect(drawer_locator).to_have_attribute("open", "", timeout=10000)
                expect(trigger_locator).to_be_focused(timeout=10000)
            finally:
                browser.close()
    finally:
        runtime.stop()


def test_persistent_drawer_allows_tab_to_reach_background_content():
    open_state = State(True)
    drawer = Drawer(
        Column(Button("Drawer action")),
        open=open_state,
        modal=False,
    )
    background = Button("Background action")
    app = Column(drawer, background)

    runtime = Runtime(
        app,
        title="PyLage Persistent Drawer Tab Browser Test",
        output="test_output/drawer_browser/persistent_tab.html",
    )

    try:
        url = runtime.start()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_function(
                    "() => window.PyLage && window.PyLage.socket && window.PyLage.socket.readyState === WebSocket.OPEN",
                    timeout=10000,
                )

                background_locator = page.locator(f'button[data-pylage-id="{background.id}"]')
                drawer_locator = page.locator(f'aside[data-pylage-id="{drawer.id}"]')
                drawer_button = drawer_locator.locator("button").first

                drawer_button.focus()
                expect(drawer_button).to_be_focused()

                page.keyboard.press("Tab")
                expect(background_locator).to_be_focused(timeout=10000)
            finally:
                browser.close()
    finally:
        runtime.stop()

def test_drawer_tab_wraps_focus_from_last_to_first():
    open_state = State(True)
    drawer = Drawer(
        Column(
            Button("First action"),
            Button("Last action"),
        ),
        open=open_state,
    )
    background = Button("Background")
    app = Column(background, drawer)

    runtime = Runtime(
        app,
        title="PyLage Drawer Focus Containment Forward Browser Test",
        output="test_output/drawer_browser/focus_containment_forward.html",
    )

    try:
        url = runtime.start()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_function(
                    "() => window.PyLage && window.PyLage.socket && window.PyLage.socket.readyState === WebSocket.OPEN",
                    timeout=10000,
                )

                drawer_locator = page.locator(
                    f"aside[data-pylage-id=\"{drawer.id}\"]"
                )
                buttons = drawer_locator.locator("button")
                first_action = buttons.nth(0)
                last_action = buttons.nth(1)


                last_action.focus()
                expect(last_action).to_be_focused()

                page.keyboard.press("Tab")


                page.wait_for_timeout(250)

                assert page.evaluate(
                    "() => document.activeElement === document.querySelector(\".pylage-drawer[open] button\")"
                )

            finally:
                browser.close()
    finally:
        runtime.stop()


def test_drawer_shift_tab_wraps_focus_from_first_to_last():
    open_state = State(True)
    drawer = Drawer(
        Column(
            Button("First action"),
            Button("Last action"),
        ),
        open=open_state,
    )
    background = Button("Background")
    app = Column(background, drawer)

    runtime = Runtime(
        app,
        title="PyLage Drawer Focus Containment Reverse Browser Test",
        output="test_output/drawer_browser/focus_containment_reverse.html",
    )

    try:
        url = runtime.start()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_function(
                    "() => window.PyLage && window.PyLage.socket && window.PyLage.socket.readyState === WebSocket.OPEN",
                    timeout=10000,
                )

                drawer_locator = page.locator(
                    f"aside[data-pylage-id=\"{drawer.id}\"]"
                )
                buttons = drawer_locator.locator("button")
                first_action = buttons.nth(0)
                last_action = buttons.nth(1)

                first_action.focus()
                expect(first_action).to_be_focused()

                page.keyboard.press("Shift+Tab")

                page.wait_for_timeout(250)

                assert page.evaluate(
                    "() => document.activeElement === document.querySelector(\".pylage-drawer[open] button:last-of-type\")"
                )
            finally:
                browser.close()
    finally:
        runtime.stop()



def test_modal_drawer_locks_body_scroll_when_opened():
    open_state = State(False)
    drawer = Drawer(
        Text("Modal drawer"),
        open=open_state,
    )
    runtime = Runtime(
        Column(drawer),
        title="PyLage Drawer Scroll Lock Browser Test",
        output="test_output/drawer_browser/scroll_lock.html",
    )

    try:
        url = runtime.start()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_function(
                    "() => window.PyLage && window.PyLage.socket && window.PyLage.socket.readyState === WebSocket.OPEN",
                    timeout=10000,
                )

                expect(page.locator("body")).to_have_css("overflow", "visible")

                open_state.set(True)

                expect(
                    page.locator("body")
                ).to_have_css("overflow", "hidden", timeout=10000)
            finally:
                browser.close()
    finally:
        runtime.stop()


def test_modal_drawer_restores_body_scroll_after_close():
    open_state = State(False)
    drawer = Drawer(
        Text("Modal drawer"),
        open=open_state,
    )
    runtime = Runtime(
        Column(drawer),
        title="PyLage Drawer Scroll Restore Browser Test",
        output="test_output/drawer_browser/scroll_restore.html",
    )

    try:
        url = runtime.start()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_function(
                    "() => window.PyLage && window.PyLage.socket && window.PyLage.socket.readyState === WebSocket.OPEN",
                    timeout=10000,
                )

                page.evaluate("document.body.style.overflow = 'scroll'")

                open_state.set(True)
                expect(
                    page.locator("body")
                ).to_have_css("overflow", "hidden", timeout=10000)

                open_state.set(False)
                expect(
                    page.locator("body")
                ).to_have_css("overflow", "scroll", timeout=10000)
            finally:
                browser.close()
    finally:
        runtime.stop()


def test_persistent_drawer_does_not_lock_body_scroll():
    open_state = State(False)
    drawer = Drawer(
        Text("Persistent drawer"),
        open=open_state,
        modal=False,
    )
    runtime = Runtime(
        Column(drawer),
        title="PyLage Persistent Drawer Scroll Browser Test",
        output="test_output/drawer_browser/persistent_scroll.html",
    )

    try:
        url = runtime.start()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_function(
                    "() => window.PyLage && window.PyLage.socket && window.PyLage.socket.readyState === WebSocket.OPEN",
                    timeout=10000,
                )

                page.evaluate("document.body.style.overflow = 'scroll'")

                open_state.set(True)

                expect(
                    page.locator("body")
                ).to_have_css("overflow", "scroll", timeout=10000)
            finally:
                browser.close()
    finally:
        runtime.stop()


def test_drawer_scrolls_long_content_without_growing_past_viewport():
    open_state = State(True)
    drawer = Drawer(
        Column(*[Text(f'Long content line {i}') for i in range(80)]),
        open=open_state,
    )
    runtime = Runtime(
        Column(drawer),
        title='PyLage Drawer Long Content Browser Test',
        output='test_output/drawer_browser/long_content.html',
    )

    try:
        url = runtime.start()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 800, 'height': 600})
            try:
                page.goto(url, wait_until='domcontentloaded')
                page.wait_for_function(
                    '() => window.PyLage && window.PyLage.socket && window.PyLage.socket.readyState === WebSocket.OPEN',
                    timeout=10000,
                )
                drawer_locator = page.locator(f'aside[data-pylage-id="{drawer.id}"]')
                expect(drawer_locator).to_have_attribute('open', '', timeout=10000)
                metrics = drawer_locator.evaluate(
                    '(element) => ({clientHeight: element.clientHeight, scrollHeight: element.scrollHeight, scrollTop: element.scrollTop})'
                )
                assert metrics['scrollHeight'] > metrics['clientHeight']
                assert metrics['scrollTop'] == 0
                scrolled = drawer_locator.evaluate(
                    '(element) => { element.scrollTop = element.scrollHeight; return element.scrollTop; }'
                )
                assert scrolled > 0
            finally:
                browser.close()
    finally:
        runtime.stop()


def test_drawer_fits_small_viewport():
    open_state = State(True)
    drawer = Drawer(
        Column(*[Text(f'Small viewport line {i}') for i in range(20)]),
        open=open_state,
    )
    runtime = Runtime(
        Column(drawer),
        title='PyLage Drawer Small Viewport Browser Test',
        output='test_output/drawer_browser/small_viewport.html',
    )

    try:
        url = runtime.start()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 320, 'height': 240})
            try:
                page.goto(url, wait_until='domcontentloaded')
                page.wait_for_function(
                    '() => window.PyLage && window.PyLage.socket && window.PyLage.socket.readyState === WebSocket.OPEN',
                    timeout=10000,
                )
                drawer_locator = page.locator(f'aside[data-pylage-id="{drawer.id}"]')
                expect(drawer_locator).to_have_attribute('open', '', timeout=10000)
                box = drawer_locator.bounding_box()
                assert box is not None
                assert box['width'] <= 320
                assert box['height'] <= 240
                assert box['x'] >= 0
                assert box['y'] >= 0
                assert box['x'] + box['width'] <= 320
                assert box['y'] + box['height'] <= 240
            finally:
                browser.close()
    finally:
        runtime.stop()

def test_responsive_drawer_uses_overlay_mode_below_breakpoint():
    open_state = State(True)
    drawer = Drawer(
        Column(
            Text("Responsive drawer"),
            Button("Action"),
        ),
        open=open_state,
        responsive_mode={"base": "overlay", "md": "persistent"},
    )
    app = Column(Button("Trigger"), drawer)

    runtime = Runtime(
        app,
        title="PyLage Responsive Drawer Mobile Browser Test",
        output="test_output/drawer_browser/responsive_mobile.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 600, "height": 800})

            try:
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_function(
                    "() => window.PyLage && window.PyLage.socket && window.PyLage.socket.readyState === WebSocket.OPEN",
                    timeout=10000,
                )

                drawer_locator = page.locator(
                    f'aside[data-pylage-id="{drawer.id}"]'
                )
                backdrop = page.locator(
                    f'.pylage-drawer-backdrop[data-pylage-drawer-id="{drawer.id}"]'
                )

                expect(drawer_locator).to_have_attribute(
                    "data-pylage-modal",
                    "true",
                )
                expect(backdrop).to_have_attribute("open", "")
                expect(page.locator("body")).to_have_css(
                    "overflow",
                    "hidden",
                )
            finally:
                browser.close()
    finally:
        runtime.stop()


def test_responsive_drawer_uses_persistent_mode_at_md_breakpoint():
    open_state = State(True)
    drawer = Drawer(
        Column(
            Text("Responsive drawer"),
            Button("Action"),
        ),
        open=open_state,
        responsive_mode={"base": "overlay", "md": "persistent"},
    )
    app = Column(Button("Trigger"), drawer)

    runtime = Runtime(
        app,
        title="PyLage Responsive Drawer Desktop Browser Test",
        output="test_output/drawer_browser/responsive_desktop.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 800, "height": 800})

            try:
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_function(
                    "() => window.PyLage && window.PyLage.socket && window.PyLage.socket.readyState === WebSocket.OPEN",
                    timeout=10000,
                )

                drawer_locator = page.locator(
                    f'aside[data-pylage-id="{drawer.id}"]'
                )
                backdrop = page.locator(
                    f'.pylage-drawer-backdrop[data-pylage-drawer-id="{drawer.id}"]'
                )

                expect(drawer_locator).to_have_attribute(
                    "data-pylage-modal",
                    "false",
                )
                expect(backdrop).not_to_have_attribute("open")
                expect(page.locator("body")).not_to_have_css(
                    "overflow",
                    "hidden",
                )
            finally:
                browser.close()
    finally:
        runtime.stop()


def test_responsive_drawer_reconciles_mode_when_viewport_crosses_breakpoint():
    open_state = State(True)
    drawer = Drawer(
        Column(
            Text("Responsive drawer"),
            Button("Action"),
        ),
        open=open_state,
        responsive_mode={"base": "overlay", "md": "persistent"},
    )
    app = Column(Button("Trigger"), drawer)

    runtime = Runtime(
        app,
        title="PyLage Responsive Drawer Resize Browser Test",
        output="test_output/drawer_browser/responsive_resize.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 600, "height": 800})

            try:
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_function(
                    "() => window.PyLage && window.PyLage.socket && window.PyLage.socket.readyState === WebSocket.OPEN",
                    timeout=10000,
                )

                drawer_locator = page.locator(
                    f'aside[data-pylage-id="{drawer.id}"]'
                )
                backdrop = page.locator(
                    f'.pylage-drawer-backdrop[data-pylage-drawer-id="{drawer.id}"]'
                )

                expect(drawer_locator).to_have_attribute(
                    "data-pylage-modal",
                    "true",
                )
                expect(backdrop).to_have_attribute("open", "")
                expect(page.locator("body")).to_have_css(
                    "overflow",
                    "hidden",
                )

                page.set_viewport_size({"width": 800, "height": 800})

                expect(drawer_locator).to_have_attribute(
                    "data-pylage-modal",
                    "false",
                    timeout=5000,
                )
                expect(backdrop).not_to_have_attribute("open")
                expect(page.locator("body")).not_to_have_css(
                    "overflow",
                    "hidden",
                )

                page.set_viewport_size({"width": 600, "height": 800})

                expect(drawer_locator).to_have_attribute(
                    "data-pylage-modal",
                    "true",
                    timeout=5000,
                )
                expect(backdrop).to_have_attribute("open")
                expect(page.locator("body")).to_have_css(
                    "overflow",
                    "hidden",
                )
            finally:
                browser.close()
    finally:
        runtime.stop()


def test_nested_modal_drawers_stack_escape_and_restore_focus():
    outer_open = State(False)
    inner_open = State(False)

    def dismiss_outer():
        outer_open.set(False)

    def dismiss_inner():
        inner_open.set(False)

    outer = Drawer(
        Text("Outer drawer"),
        Button("Outer action"),
        open=outer_open,
        on_dismiss=dismiss_outer,
    )
    inner = Drawer(
        Text("Inner drawer"),
        Button("Inner action"),
        open=inner_open,
        on_dismiss=dismiss_inner,
    )
    trigger = Button("Open outer")

    runtime = Runtime(
        Column(trigger, outer, inner),
        title="PyLage Nested Modal Drawer Browser Test",
        output="test_output/drawer_browser/nested_modal.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_function(
                    """() => (
                        window.PyLage &&
                        window.PyLage.socket &&
                        window.PyLage.socket.readyState === WebSocket.OPEN
                    )""",
                    timeout=10000,
                )

                trigger_locator = page.get_by_role("button", name="Open outer")
                outer_locator = page.locator(
                    f'aside[data-pylage-id="{outer.id}"]'
                )
                inner_locator = page.locator(
                    f'aside[data-pylage-id="{inner.id}"]'
                )

                trigger_locator.focus()
                expect(trigger_locator).to_be_focused()

                outer_open.set(True)
                expect(
                    outer_locator.locator("button").first
                ).to_be_focused(timeout=10000)

                inner_open.set(True)
                inner_action = inner_locator.locator("button").first
                outer_action = outer_locator.locator("button").first

                expect(inner_action).to_be_focused(timeout=10000)

                expect(outer_locator).to_have_attribute("open", "")
                expect(inner_locator).to_have_attribute("open", "")

                modal_drawers = page.locator(
                    '.pylage-drawer[open][data-pylage-modal="true"]'
                )
                expect(modal_drawers).to_have_count(2)

                page.keyboard.press("Escape")

                expect(inner_locator).not_to_have_attribute(
                    "open",
                    timeout=10000,
                )
                expect(outer_locator).to_have_attribute("open", "")
                expect(outer_action).to_be_focused(timeout=10000)

                page.keyboard.press("Escape")

                expect(outer_locator).not_to_have_attribute(
                    "open",
                    timeout=10000,
                )
                expect(trigger_locator).to_be_focused(timeout=10000)

            finally:
                browser.close()
    finally:
        runtime.stop()
