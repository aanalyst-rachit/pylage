from __future__ import annotations

import pylage as pl

import csv
from pathlib import Path



def _load_test_csv():
    csv_path = Path(__file__).resolve().parents[1] / "data" / "test.csv"

    with csv_path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def get_app():
    rows = _load_test_csv()

    return pl.column(
        pl.text(
            "DataFrame",
            style=pl.style(
                font_size="2rem",
                font_weight="700",
                color="#0f172a",
                font_family="Inter, sans-serif",
            ),
        ),
        pl.text(
            "Excel-like data grid using the project's real test.csv dataset.",
            style=pl.style(
                color="#64748b",
                margin_bottom="1.5rem",
                font_family="Inter, sans-serif",
            ),
        ),
        pl.text(
            "Cell borders — default ON",
            style=pl.style(
                font_size="1.1rem",
                font_weight="600",
                color="#0f172a",
                font_family="Inter, sans-serif",
            ),
        ),
        pl.dataframe(
            rows,
            title="test.csv — bordered grid",
            class_name="test-csv-grid",
        ),
        pl.text(
            "Cell borders — OFF",
            style=pl.style(
                font_size="1.1rem",
                font_weight="600",
                color="#0f172a",
                margin_top="1.5rem",
                font_family="Inter, sans-serif",
            ),
        ),
        pl.dataframe(
            rows[:8],
            title="test.csv — no cell borders",
            cell_border=False,
            class_name="test-csv-grid-no-border",
        ),
        pl.text(
            "Verify: the outer DataFrame border remains visible while "
            "individual cell borders are disabled.",
            style=pl.style(
                color="#64748b",
                margin_top="1rem",
                font_size="0.875rem",
                font_family="Inter, sans-serif",
            ),
        ),
        style=pl.style(
            padding="2rem",
            max_width="1100px",
            margin="0 auto",
            font_family="Inter, sans-serif",
            display="flex",
            flex_direction="column",
            gap="0.75rem",
        ),
    )
