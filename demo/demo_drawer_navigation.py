import pylage as pl
import pylage as ps



def get_app():

    drawer_open = ps.State(False)
    navigation_open = ps.State(False)
    mobile_open = ps.State(False)

    status = ps.State("Select a Drawer API to test.")

    def open_drawer(state, name):

        def handler(e=None):
            drawer_open.set(False)
            navigation_open.set(False)
            mobile_open.set(False)

            state.set(True)
            status.set(f"{name} is OPEN.")

        return handler

    def close_drawer(state, name):

        def handler(e=None):
            state.set(False)
            status.set(f"{name} is CLOSED.")

        return handler

    # ============================================================
    # GENERIC DRAWER
    # ============================================================

    drawer_content = pl.column(
        pl.heading("drawer", level=2),
        pl.text("Generic UI Kit Drawer"),
        pl.text("Rendered through ps.drawer()."),
        pl.button(
            "Close",
            on_click=close_drawer(drawer_open, "drawer"),
        ),
        style=pl.style(
            padding="1.5rem",
            gap="0.75rem",
            width="320px",
            height="100vh",
            background="#ffffff",
        ),
    )

    # ============================================================
    # NAVIGATION DRAWER
    # ============================================================

    navigation_content = pl.column(
        pl.heading("navigation_drawer", level=2),
        pl.text("Navigation Drawer"),
        pl.text("Rendered through ps.navigation_drawer()."),
        pl.button(
            "Dashboard",
            on_click=close_drawer(
                navigation_open,
                "navigation_drawer",
            ),
        ),
        pl.button(
            "Users",
            on_click=close_drawer(
                navigation_open,
                "navigation_drawer",
            ),
        ),
        pl.button(
            "Settings",
            on_click=close_drawer(
                navigation_open,
                "navigation_drawer",
            ),
        ),
        pl.button(
            "Close",
            on_click=close_drawer(
                navigation_open,
                "navigation_drawer",
            ),
            variant="secondary",
        ),
        style=pl.style(
            padding="1.5rem",
            gap="0.75rem",
            width="320px",
            height="100vh",
            background="#ffffff",
        ),
    )

    # ============================================================
    # MOBILE SIDEBAR
    # ============================================================

    mobile_content = pl.column(
        pl.heading("mobile_sidebar", level=2),
        pl.text("Mobile Sidebar"),
        pl.text("Rendered through ps.mobile_sidebar()."),
        pl.button(
            "Close",
            on_click=close_drawer(
                mobile_open,
                "mobile_sidebar",
            ),
        ),
        style=pl.style(
            padding="1.5rem",
            gap="0.75rem",
            width="320px",
            height="100vh",
            background="#ffffff",
        ),
    )

    # ============================================================
    # APP
    # ============================================================

    return pl.column(
        pl.heading(
            "UI Kit Drawer — Manual Verification",
            level=1,
        ),

        pl.text(
            status,
            style=pl.style(
                font_size="1.1rem",
                font_weight="bold",
            ),
        ),

        pl.button(
            "Open drawer()",
            on_click=open_drawer(
                drawer_open,
                "drawer",
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

        getattr(ps, "drawer")(
            drawer_content,
            open=drawer_open,
            title="drawer",
            class_name="manual-drawer",
        ),

        getattr(ps, "navigation_drawer")(
            navigation_content,
            open=navigation_open,
            title="navigation_drawer",
            class_name="manual-navigation-drawer",
        ),

        getattr(ps, "mobile_sidebar")(
            mobile_content,
            open=mobile_open,
            title="mobile_sidebar",
            class_name="manual-mobile-sidebar",
        ),

        style=pl.style(
            padding="2rem",
            gap="1rem",
            min_height="100vh",
            background="#F9FAFB",
        ),
    )


if __name__ == "__main__":
    ps.run(
        get_app(),
        title="PyLage UI Kit Drawer Manual",
        serve=True,
        host="0.0.0.0",
        port=3000,
    )
