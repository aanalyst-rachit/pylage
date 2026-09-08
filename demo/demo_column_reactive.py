import pylage as pl
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps




def get_app():
    gap = pl.state("1rem")
    column_color = pl.state("#dbeafe")
    status = pl.state("Column wrapper is working.")

    def toggle_gap(e=None):
        print("CLICK RECEIVED", e)
        print("GAP BEFORE", gap.value)
        next_gap = "2rem" if gap.value == "1rem" else "1rem"
        next_color = "#dcfce7" if column_color.value == "#dbeafe" else "#dbeafe"
        gap.set(next_gap)
        column_color.set(next_color)
        status.set(f"Reactive gap changed to {next_gap}.")
        print("GAP AFTER", gap.value)
        print("COLOR AFTER", column_color.value)
        print("STATUS AFTER", status.value)

    content = pl.column(
        pl.heading("Column Wrapper", level=2),
        pl.text("This content is rendered through the UI Kit pl.column() wrapper."),
        pl.row(
            pl.text("Status: ", style=pl.style(font_weight="bold")),
            pl.text(status, style=pl.style(font_weight="bold")),
            style=pl.style(display="flex", align_items="center", gap="0.5rem"),
        ),
        pl.button("Change Gap Reactively", on_click=toggle_gap, variant="primary"),
        style=pl.style(display="flex", flex_direction="column", gap=gap, padding="1.5rem", min_height="300px", background_color=column_color, border="3px solid #2563eb"),
        class_name="pylage-ui-kit-column-test",
    )

    app = pl.column(
        pl.heading("UI Kit Column — Manual Test", level=1),
        pl.text("Testing wrapper reuse, child composition, props, and reactive styles."),
        pl.card(content, style=pl.style(padding="1rem", margin_top="1rem")),
        style=pl.style(padding="2rem", gap="1.5rem", font_family="system-ui, sans-serif"),
    )

    return app


if __name__ == "__main__":
    app = get_app()
    ps.run(app, title="PyLage UI Kit Column Manual", serve=True, host="0.0.0.0", port=3000)
