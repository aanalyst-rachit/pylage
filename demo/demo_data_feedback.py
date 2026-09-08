import pylage as pl


def get_app():
    # --- Reactive States ---
    toast_visible = pl.state(True)
    progress_val = pl.state(45)

    def close_toast():
        toast_visible.set(False)

    def boost_progress():
        if progress_val.value >= 100:
            progress_val.set(10)
        else:
            progress_val.set(progress_val.value + 15)

    # --- UI Layout ---
    app = pl.column(style=pl.style(padding="24px", gap="24px", max_width="900px", margin="0 auto"))

    # Header
    app.add(
        pl.heading("📊 Data & Feedback Components Live Demo", level=2),
        pl.text("Interactive showcase for testing component visual output and state integration.")
    )

    # 1. Table Component
    app.add(
        pl.card(
            pl.heading("1. Table Component", level=3),
            pl.table(
                headers=["ID", "User", "Role", "Status"],
                rows=[
                    ["101", "Rachit", "Admin", "Active"],
                    ["102", "Alex", "Developer", "Pending"],
                    ["103", "Sarah", "Designer", "Active"],
                ],
                style=pl.style(margin_top="12px", width="100%")
            )
        )
    )

    # 2. Alert Component
    app.add(
        pl.card(
            pl.heading("2. Alert Component", level=3),
            pl.column(
                pl.alert("Success! Your changes have been saved cleanly.", variant="success"),
                pl.alert("Warning: Low disk space remaining on server.", variant="warning"),
                pl.alert("Error: Failed to connect to local WebSocket.", variant="error"),
                style=pl.style(gap="8px", margin_top="12px")
            )
        )
    )

    # 3. Toast Component
    app.add(
        pl.card(
            pl.heading("3. Toast Component", level=3),
            pl.column(
                pl.toast(
                    "Notification: pl.State update broadcast successfully!",
                    visible=toast_visible,
                    on_click=close_toast
                ),
                pl.button("Dismiss / Toggle Toast pl.State", on_click=close_toast, style=pl.style(margin_top="8px"))
            )
        )
    )

    # 4. Spinner Component
    app.add(
        pl.card(
            pl.heading("4. Spinner Component", level=3),
            pl.row(
                pl.spinner(size="sm"),
                pl.spinner(size="md"),
                pl.spinner(size="lg"),
                style=pl.style(gap="16px", align_items="center", margin_top="12px")
            )
        )
    )

    # 5. ProgressBar Component
    app.add(
        pl.card(
            pl.heading("5. ProgressBar Component", level=3),
            pl.column(
                pl.progress_bar(value=progress_val, max=100),
                pl.button("Boost Progress pl.State (+15%)", on_click=boost_progress, style=pl.style(margin_top="8px"))
            )
        )
    )

    # 6. Skeleton Component
    app.add(
        pl.card(
            pl.heading("6. Skeleton Component", level=3),
            pl.column(
                pl.skeleton(height="20px", width="60%"),
                pl.skeleton(height="14px", width="100%"),
                pl.skeleton(height="14px", width="85%"),
                style=pl.style(gap="8px", margin_top="12px")
            )
        )
    )

    # 7. Badge Component
    app.add(
        pl.card(
            pl.heading("7. Badge Component", level=3),
            pl.row(
                pl.badge("New", variant="primary"),
                pl.badge("Completed", variant="success"),
                pl.badge("In Progress", variant="warning"),
                pl.badge("Deprecated", variant="danger"),
                style=pl.style(gap="8px", margin_top="12px")
            )
        )
    )

    # 8. Accordion Component
    app.add(
        pl.card(
            pl.heading("8. Accordion Component", level=3),
            pl.accordion(
                items=[
                    {"title": "Section 1: Architecture Overview", "content": "PyLage utilizes WebSocket reactive tree patching."},
                    {"title": "Section 2: pl.State Management", "content": "pl.State binding maps dependencies directly to DOM attributes."},
                ],
                style=pl.style(margin_top="12px")
            )
        )
    )

    # 9. Carousel Component
    app.add(
        pl.card(
            pl.heading("9. Carousel Component", level=3),
            pl.carousel(
                items=[
                    pl.card(pl.text("Slide 1: Real-time UI Engine")),
                    pl.card(pl.text("Slide 2: Reactive WebSockets")),
                    pl.card(pl.text("Slide 3: High Performance Diffing")),
                ],
                style=pl.style(margin_top="12px")
            )
        )
    )

    return app
