import pylage as pl
import sys
from pathlib import Path

# Project root setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps


def get_app():
    # pl.State Management
    current_page = pl.State(1)
    total_pages = 5
    page_data_msg = pl.State("Showing Records 1 - 10 of 50")

    def go_prev(e=None):
        if current_page.value > 1:
            p = current_page.value - 1
            current_page.set(p)
            page_data_msg.set(f"Showing Records {(p-1)*10 + 1} - {p*10} of 50")

    def go_next(e=None):
        if current_page.value < total_pages:
            p = current_page.value + 1
            current_page.set(p)
            page_data_msg.set(f"Showing Records {(p-1)*10 + 1} - {p*10} of 50")

    def jump_page(p_val):
        def handler(e=None):
            current_page.set(p_val)
            page_data_msg.set(f"Showing Records {(p_val-1)*10 + 1} - {p_val*10} of 50")
        return handler

    # pl.breadcrumb_trail
    crumbs = pl.breadcrumb_trail(
        pl.text("Home / "),
        pl.text("Admin / "),
        pl.text("Users / "),
        pl.text("Paginated View"),
        style=pl.style(font_size="0.875rem", color="#64748b", margin_bottom="1rem")
    )

    # pl.pagination controls
    page_buttons = [
        pl.button("◀ Prev", on_click=go_prev, variant="secondary"),
    ]
    for i in range(1, total_pages + 1):
        page_buttons.append(pl.button(str(i), on_click=jump_page(i)))
    page_buttons.append(pl.button("Next ▶", on_click=go_next, variant="secondary"))

    pag_row = pl.row(*page_buttons, style=pl.style(display="flex", gap="0.5rem", align_items="center", justify_content="center"))

    pagination_node = pl.pagination(
        pag_row,
        class_name="pylage-pagination-bar",
        title="Table pl.pagination",
        style=pl.style(width="100%", margin_top="1rem")
    )

    app = pl.column(
        crumbs,
        pl.heading("pl.pagination & pl.breadcrumb_trail — Live Manual Test Suite", level=1),
        pl.text("Test page navigation, stepper bounds clamping, and breadcrumbs trail rendering."),
        pl.card(
            pl.row(
                pl.text("Current Page: ", style=pl.style(font_weight="bold")),
                pl.heading(current_page, level=3, style=pl.style(color="#2563eb", margin="0")),
                pl.text(f" of {total_pages}", style=pl.style(color="#64748b")),
                style=pl.style(display="flex", align_items="center", gap="0.5rem")
            ),
            pl.row(
                pl.text("Record Subset: ", style=pl.style(font_weight="bold")),
                pl.text(page_data_msg, style=pl.style(color="#10b981", font_weight="bold")),
                style=pl.style(display="flex", align_items="center", gap="0.5rem", margin_top="0.5rem")
            ),
            style=pl.style(padding="1rem", background="#f8fafc", border_radius="8px", margin_bottom="1.5rem")
        ),
        pagination_node,
        style=pl.style(padding="2rem", gap="1.5rem", font_family="system-ui, sans-serif")
    )

    return app


if __name__ == "__main__":
    app = get_app()
    ps.run(app, title="PyLage pl.pagination Manual Test", serve=True, host="0.0.0.0", port=3000)
