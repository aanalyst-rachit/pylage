from __future__ import annotations

from playwright.sync_api import expect, sync_playwright

import pylage as pl
from pylage.ENGINE.runtime import Runtime


def test_form_browser_render_and_submit():
    submitted = pl.State("Not submitted")

    def handle_submit(payload):
        if isinstance(payload, dict):
            values = payload.get("values", {})
            submitted.set(str(values.get("email", "")))

    app = pl.form(
        pl.form_field(
            pl.input(
                name="email",
                value="initial@example.com",
                placeholder="Email address",
            ),
            label="Email",
            required=True,
            help_text="Use your work email.",
        ),
        pl.button("Submit", type="submit"),
        pl.text(submitted),
        on_submit=handle_submit,
    )

    runtime = Runtime(
        app,
        title="PyLage Form Browser Test",
        output="test_output/form_browser/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                page.goto(url)

                assert page.locator("form").count() == 1
                assert page.locator("input").count() == 1
                assert page.locator("button").count() == 1

                email = page.locator("input").first
                expect(email).to_have_value("initial@example.com")

                email.fill("updated@example.com")
                expect(email).to_have_value("updated@example.com")

                page.locator("button").first.click()

                expect(page.locator("body")).to_contain_text(
                    "updated@example.com"
                )

            finally:
                browser.close()

    finally:
        runtime.stop()
