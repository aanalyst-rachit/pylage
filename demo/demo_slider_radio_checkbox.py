import pylage as pl
"""Manual demo for PyLage pl.input Controls (pl.slider, pl.radio_group, pl.checkbox, pl.switch, pl.datepicker)."""



def get_app() -> pl.column:
    slider_val = pl.state(45)
    selected_plan = pl.state("pro")
    agree_terms = pl.state(True)
    enable_notifications = pl.state(True)
    selected_date = pl.state("2026-09-01")

    title = pl.heading("🎛️ Form & Interactive Controls Manual", level=1)
    desc = pl.text(
        "Demonstrates pl.slider, pl.radio_group, pl.checkbox, pl.switch, and pl.datepicker interactive two-way bindings.",
        style=pl.style(color="#64748b", margin_bottom="1.5rem"),
    )

    # 1. pl.slider Control
    slider_card = pl.card(
        pl.heading("1. pl.slider & Range pl.input", level=3),
        pl.row(
            pl.text("Volume / Threshold: "),
            pl.badge(slider_val, variant="primary"),
            style=pl.style(align_items="center", gap="0.75rem", margin_bottom="0.5rem"),
        ),
        pl.slider(
            min=0,
            max=100,
            step=1,
            value=slider_val,
            on_change=lambda e: slider_val.set(int(e.get("value", 0))),
            style=pl.style(width="100%"),
        ),
        style=pl.style(padding="1.25rem", margin_bottom="1rem", background="#ffffff", border="1px solid #e2e8f0", border_radius="0.75rem"),
    )

    # 2. pl.radio_group & pl.checkbox
    options_card = pl.card(
        pl.heading("2. pl.radio_group & pl.checkbox Controls", level=3),
        pl.text("Select Subscription Tier:"),
        pl.radio_group(
            name="plan",
            options=["starter", "pro", "enterprise"],
            value=selected_plan,
            on_change=lambda e: selected_plan.set(e.get("value", "pro")),
            style=pl.style(margin_top="0.5rem", margin_bottom="1rem"),
        ),
        pl.row(
            pl.checkbox(
                checked=agree_terms,
                on_change=lambda e: agree_terms.set(e.get("checked", False)),
            ),
            pl.text("I agree to the Terms of Service & Privacy Policy"),
            style=pl.style(align_items="center", gap="0.5rem", margin_bottom="0.5rem"),
        ),
        pl.row(
            pl.switch(
                checked=enable_notifications,
                on_change=lambda e: enable_notifications.set(e.get("checked", False)),
            ),
            pl.text("Enable Real-Time Push Notifications"),
            style=pl.style(align_items="center", gap="0.5rem"),
        ),
        style=pl.style(padding="1.25rem", margin_bottom="1rem", background="#ffffff", border="1px solid #e2e8f0", border_radius="0.75rem"),
    )

    # 3. pl.datepicker Control
    date_card = pl.card(
        pl.heading("3. pl.datepicker Calendar Control", level=3),
        pl.row(
            pl.text("Selected Deployment Date: "),
            pl.badge(selected_date, variant="secondary"),
            style=pl.style(align_items="center", gap="0.75rem", margin_bottom="0.75rem"),
        ),
        pl.datepicker(
            value=selected_date,
            on_change=lambda e: selected_date.set(e.get("value", "")),
            style=pl.style(padding="0.5rem", border="1px solid #cbd5e1", border_radius="0.375rem"),
        ),
        style=pl.style(padding="1.25rem", margin_bottom="1rem", background="#ffffff", border="1px solid #e2e8f0", border_radius="0.75rem"),
    )

    return pl.column(
        title,
        desc,
        slider_card,
        options_card,
        date_card,
        style=pl.style(padding="2rem", max_width="900px", margin="0 auto"),
    )
