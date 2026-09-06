import pylage as pl


def get_app():
    status = pl.State("Selected: Home")

    home_active = pl.State(True)
    products_active = pl.State(False)
    settings_active = pl.State(False)
    profile_active = pl.State(False)

    def select_item(name, selected_state, other_states):
        def handler(e=None):
            selected_state.set(True)
            for state in other_states:
                state.set(False)
            status.set(f"Selected: {name}")
        return handler

    home = pl.navigation_item(
        "Home",
        active=home_active,
        on_click=select_item(
            "Home",
            home_active,
            [products_active, settings_active, profile_active],
        ),
    )

    products = pl.navigation_item(
        "Products",
        active=products_active,
        on_click=select_item(
            "Products",
            products_active,
            [home_active, settings_active, profile_active],
        ),
    )

    settings = pl.navigation_item(
        "Settings",
        active=settings_active,
        on_click=select_item(
            "Settings",
            settings_active,
            [home_active, products_active, profile_active],
        ),
    )

    profile = pl.navigation_item(
        "Profile",
        active=profile_active,
        on_click=select_item(
            "Profile",
            profile_active,
            [home_active, products_active, settings_active],
        ),
    )

    return pl.column(
        pl.heading("UI Kit Navigation Item — Manual Verification"),
        pl.text("Click an item. The selected item should become active and blue."),
        pl.text(status),
        pl.row(home, products, settings, profile),
    )


if __name__ == "__main__":
    pl.run(
        get_app(),
        title="PyLage UI Kit Navigation Item Manual",
        serve=True,
        host="0.0.0.0",
        port=3000,
    )
