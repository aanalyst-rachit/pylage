import pylage as pl


label = "Drawer Home"


def page():
    drawer_open = pl.state(False)
    navigation_open = pl.state(False)
    mobile_open = pl.state(False)
    status = pl.state("No drawer is open.")

    def close_all():
        drawer_open.set(False)
        navigation_open.set(False)
        mobile_open.set(False)

    def open_drawer(state, name):
        def handler(e=None):
            close_all()
            state.set(True)
            status.set(f"{name} is OPEN.")

        return handler

    def close_drawer(state, name):
        def handler(e=None):
            state.set(False)
            status.set(f"{name} is CLOSED.")

        return handler

    generic_content = pl.column(
        pl.row(
            pl.image(
                src="https://commons.wikimedia.org/wiki/Special:Redirect/file/SVG_Simple_Logo.svg",
                alt="Open SVG logo",
                style=pl.style(
                    width="48px",
                    height="48px",
                    object_fit="contain",
                ),
            ),
            pl.column(
                pl.heading("Generic Drawer", level=2),
                pl.text("Custom remote image in the Drawer header."),
                style=pl.style(gap="0.2rem"),
            ),
            style=pl.style(
                display="flex",
                align_items="center",
                gap="0.75rem",
            ),
        ),
        pl.text("Live test of pl.drawer()."),
        pl.navigation_item("Dashboard", href="/dashboard"),
        pl.navigation_item("Projects", href="/projects"),
        pl.navigation_item("Settings", href="/settings"),
        pl.button(
            "Close drawer",
            on_click=close_drawer(drawer_open, "drawer"),
            variant="secondary",
        ),
        style=pl.style(
            padding="1.5rem",
            gap="0.8rem",
            width="320px",
            height="100vh",
            background="#ffffff",
        ),
    )

    navigation_content = pl.column(
        pl.heading("Navigation Drawer", level=2),
        pl.text("Live test of pl.navigation_drawer()."),
        pl.navigation_item("Home", href="/"),
        pl.navigation_item("Dashboard", href="/dashboard"),
        pl.navigation_item("Projects", href="/projects"),
        pl.navigation_item("Settings", href="/settings"),
        pl.button(
            "Close navigation drawer",
            on_click=close_drawer(
                navigation_open,
                "navigation_drawer",
            ),
            variant="secondary",
        ),
        style=pl.style(
            padding="1.5rem",
            gap="0.8rem",
            width="320px",
            height="100vh",
            background="#ffffff",
        ),
    )

    mobile_content = pl.column(
        pl.heading("Mobile Sidebar", level=2),
        pl.text("Live test of pl.mobile_sidebar()."),
        pl.navigation_item("Home", href="/"),
        pl.navigation_item("Dashboard", href="/dashboard"),
        pl.navigation_item("Projects", href="/projects"),
        pl.button(
            "Close mobile sidebar",
            on_click=close_drawer(
                mobile_open,
                "mobile_sidebar",
            ),
            variant="secondary",
        ),
        style=pl.style(
            padding="1.5rem",
            gap="0.8rem",
            width="300px",
            height="100vh",
            background="#ffffff",
        ),
    )

    return pl.column(
        pl.heading(
            "PyLage Drawer — Live Browser Test",
            level=1,
        ),
        pl.text(
            "Public API only: drawer(), navigation_drawer(), "
            "mobile_sidebar(), state(), navigation_item().",
        ),
        pl.card(
            pl.column(
                pl.text(
                    "Live status",
                    style=pl.style(font_weight="bold"),
                ),
                pl.text(
                    status,
                    style=pl.style(
                        font_size="1.1rem",
                        font_weight="bold",
                    ),
                ),
                style=pl.style(gap="0.4rem"),
            ),
            style=pl.style(
                padding="1rem",
                margin_bottom="1rem",
            ),
        ),
        pl.row(
            pl.button(
                "Open drawer()",
                on_click=open_drawer(drawer_open, "drawer"),
            ),
            pl.column(
                pl.image(
                    src="https://commons.wikimedia.org/wiki/Special:Redirect/file/SVG_Simple_Logo.svg",
                    alt="Open drawer",
                    style=pl.style(
                        width="32px",
                        height="32px",
                        object_fit="contain",
                    ),
                ),
                on_click=open_drawer(drawer_open, "drawer"),
                title="Open drawer with image",
                style=pl.style(
                    cursor="pointer",
                    padding="0.35rem",
                ),
            ),
            pl.button(
                "Open navigation_drawer()",
                on_click=open_drawer(
                    navigation_open,
                    "navigation_drawer",
                ),
            ),
            pl.button(
                "Open mobile_sidebar()",
                on_click=open_drawer(
                    mobile_open,
                    "mobile_sidebar",
                ),
            ),
            style=pl.style(
                display="flex",
                gap="0.75rem",
                flex_wrap="wrap",
            ),
        ),
        pl.drawer(
            generic_content,
            open=drawer_open,
            title="Drawer",
            class_name="live-drawer",
        ),
        pl.navigation_drawer(
            navigation_content,
            open=navigation_open,
            title="Navigation Drawer",
            class_name="live-navigation-drawer",
        ),
        pl.mobile_sidebar(
            mobile_content,
            open=mobile_open,
            title="Mobile Sidebar",
            class_name="live-mobile-sidebar",
            responsive_mode={"base": "overlay", "md": "persistent"},
        ),
        style=pl.style(
            padding="2rem",
            gap="1rem",
            min_height="100vh",
            background="#f8fafc",
            font_family="system-ui, sans-serif",
        ),
    )
