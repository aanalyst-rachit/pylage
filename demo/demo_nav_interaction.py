import pylage as pl
from pathlib import Path
from pylage.ENGINE.core.component import component


def get_nav_interaction_app():
    # -------------------------------------------------------------
    # REACTIVE STATES
    # -------------------------------------------------------------
    active_tab = pl.State("tab1")
    current_page = pl.State(1)
    drawer_open = pl.State(False)
    dialog_open = pl.State(False)
    popover_open = pl.State(False)
    menu_selected = pl.State("Home")

    # -------------------------------------------------------------
    # EVENT HANDLERS
    # -------------------------------------------------------------
    def set_tab(tab_name):
        return lambda payload=None: active_tab.set(tab_name)

    def change_page(delta):
        def handler(payload=None):
            new_pg = max(1, current_page.value + delta)
            current_page.set(new_pg)

        return handler

    def toggle_drawer(payload=None):
        drawer_open.set(not drawer_open.value)

    def toggle_dialog(payload=None):
        dialog_open.set(not dialog_open.value)

    def toggle_popover(payload=None):
        popover_open.set(not popover_open.value)

    def select_menu_item(item):
        return lambda payload=None: menu_selected.set(item)

    # -------------------------------------------------------------
    # UI COMPONENTS LAYOUT
    # -------------------------------------------------------------
    return pl.column(
        pl.heading("PyLage Navigation & Interaction Components Demo"),
        # 1. NAVIGATION & BREADCRUMBS
        pl.card(
            pl.heading("1. Navigation & Breadcrumbs"),
            pl.row(
                pl.text("Home"),
                pl.text(" > "),
                pl.text("Dashboard"),
                pl.text(" > "),
                pl.text("Settings"),
                class_name="breadcrumbs",
            ),
            class_name="demo-card",
        ),
        # 2. TABS COMPONENT
        pl.card(
            pl.heading("2. Tabs Component"),
            pl.row(
                pl.button("Tab 1", on_click=set_tab("tab1")),
                pl.button("Tab 2", on_click=set_tab("tab2")),
                pl.button("Tab 3", on_click=set_tab("tab3")),
            ),
            pl.text("Active Tab Payload: "),
            pl.text(active_tab),
            class_name="demo-card",
        ),
        # 3. PAGINATION COMPONENT
        pl.card(
            pl.heading("3. Pagination Component"),
            pl.row(
                pl.button("Previous", on_click=change_page(-1)),
                pl.text(" Page "),
                pl.text(current_page),
                pl.text(" "),
                pl.button("Next", on_click=change_page(1)),
            ),
            class_name="demo-card",
        ),
        # 4. MENU COMPONENT
        pl.card(
            pl.heading("4. Menu Component"),
            pl.row(
                pl.button("Profile", on_click=select_menu_item("Profile")),
                pl.button("Settings", on_click=select_menu_item("Settings")),
                pl.button("Logout", on_click=select_menu_item("Logout")),
            ),
            pl.text("Selected Menu: "),
            pl.text(menu_selected),
            class_name="demo-card",
        ),
        # 5. DRAWER COMPONENT
        pl.card(
            pl.heading("5. Drawer Component"),
            pl.button("Toggle Drawer", on_click=toggle_drawer),
            pl.text("Drawer Visible pl.State: "),
            pl.text(drawer_open),
            class_name="demo-card",
        ),
        # 6. TOOLTIP & POPOVER COMPONENT
        pl.card(
            pl.heading("6. Tooltip & Popover Component"),
            pl.row(
                component(
                    "span",
                    "Hover over me (Tooltip)",
                    title="This is a native tooltip message",
                ),
                pl.button("Toggle Popover", on_click=toggle_popover),
            ),
            pl.text("Popover Active: "),
            pl.text(popover_open),
            class_name="demo-card",
        ),
        # 7. DIALOG / MODAL COMPONENT
        pl.card(
            pl.heading("7. Dialog / Modal Component"),
            pl.button("Open Dialog Modal", on_click=toggle_dialog),
            pl.text("Dialog Open pl.State: "),
            pl.text(dialog_open),
            class_name="demo-card",
        ),
        class_name="container",
    )


def get_app():
    return get_nav_interaction_app()
