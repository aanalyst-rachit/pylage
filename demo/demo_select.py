import pylage as pl
import sys
from pathlib import Path

# Project root setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps


def get_app():
    # -------------------------------------------------------------------------
    # pl.State Management
    # -------------------------------------------------------------------------
    selected_language = pl.state("Python")
    selected_database = pl.state("postgresql")

    # pl.State Handlers
    def handle_language_change(val):
        clean_val = val.get("value", val) if isinstance(val, dict) else str(val)
        selected_language.set(clean_val)

    def handle_database_change(val):
        clean_val = val.get("value", val) if isinstance(val, dict) else str(val)
        selected_database.set(clean_val)

    # -------------------------------------------------------------------------
    # Native PyLage pl.select Generator
    # -------------------------------------------------------------------------
    def build_select(options_list, current_state, on_change_fn):

        if hasattr(pl, "select"):
            try:
                option_children = []
                for opt in options_list:
                    val = opt.get("value") if isinstance(opt, dict) else opt
                    lbl = opt.get("label") if isinstance(opt, dict) else opt
                    option_children.append(pl.option(lbl, value=val))

                return pl.select(
                    *option_children,           # ✅ actual <option> children
                    value=current_state,        # ✅ pl.State object, not .value
                    on_change=on_change_fn,
                    style=pl.style(
                        width="100%",
                        padding="0.6rem",
                        border="1px solid #cbd5e1",
                        border_radius="0.375rem",
                        background_color="#ffffff",
                        color="#0f172a",
                        font_size="0.95rem",
                        cursor="pointer",
                    ),
                )
            except Exception:
                pass
        # 2. Native Component Builder with raw HTML props

        select_node = pl.select(*[pl.option(opt.get("label") if isinstance(opt, dict) else opt, value=opt.get("value") if isinstance(opt, dict) else opt) for opt in options_list], value=current_state, on_change=on_change_fn)
        return select_node


        # pl.style dict injection directly inside props
        select_node.props["style"] = {
            "width": "100%",
            "padding": "0.6rem",
            "border": "1px solid #cbd5e1",
            "borderRadius": "0.375rem",
            "backgroundColor": "#ffffff",
            "color": "#0f172a",
            "fontSize": "0.95rem",
            "cursor": "pointer",
        }

        # Build options
        for opt in options_list:
            val = opt.get("value") if isinstance(opt, dict) else opt
            lbl = opt.get("label") if isinstance(opt, dict) else opt

            opt_node = Component("option")
            opt_node.props["value"] = str(val)
            opt_node.children = [str(lbl)]

            if str(val) == str(current_state.value):
                opt_node.props["selected"] = True

            select_node.children.append(opt_node)

        return select_node

    # -------------------------------------------------------------------------
    # UI Layout
    # -------------------------------------------------------------------------
    return pl.column(
        pl.heading(
            "pl.select (Dropdown) Component Demo",
            style=pl.style(
                font_size="1.75rem",
                font_weight="800",
                color="#0f172a",
                margin_bottom="0.25rem",
            ),
        ),
        pl.text(
            "Interactive demonstration of single-select dropdown state in PyLage.",
            style=pl.style(color="#64748b", font_size="0.9rem", margin_bottom="1.5rem"),
        ),

        # DEMO 1: Simple Options
        pl.column(
            pl.row(
                pl.text("Selected Language: ", style=pl.style(font_weight="500", color="#475569")),
                pl.text(selected_language, style=pl.style(color="#2563eb", font_weight="700")),
                style=pl.style(gap="0.5rem", align_items="center", margin_bottom="0.75rem"),
            ),
            build_select(
                options_list=["Python", "JavaScript", "Rust", "Go", "C++"],
                current_state=selected_language,
                on_change_fn=handle_language_change,
            ),
            style=pl.style(
                padding="1rem",
                background_color="#ffffff",
                border="1px solid #e2e8f0",
                border_radius="0.5rem",
                margin_bottom="1.5rem",
                width="100%",
            ),
        ),

        # DEMO 2: Key-Value Options
        pl.column(
            pl.row(
                pl.text("Selected Database: ", style=pl.style(font_weight="500", color="#475569")),
                pl.text(selected_database, style=pl.style(color="#059669", font_weight="700")),
                style=pl.style(gap="0.5rem", align_items="center", margin_bottom="0.75rem"),
            ),
            build_select(
                options_list=[
                    {"label": "PostgreSQL (Relational)", "value": "postgresql"},
                    {"label": "MongoDB (NoSQL Document)", "value": "mongodb"},
                    {"label": "Redis (In-Memory Data Store)", "value": "redis"},
                    {"label": "SQLite (Embedded DB)", "value": "sqlite"},
                ],
                current_state=selected_database,
                on_change_fn=handle_database_change,
            ),
            style=pl.style(
                padding="1rem",
                background_color="#ffffff",
                border="1px solid #e2e8f0",
                border_radius="0.5rem",
                width="100%",
            ),
        ),

        style=pl.style(
            width="100%",
            max_width="560px",
            padding="2rem",
            background_color="#f8fafc",
            border_radius="0.75rem",
            box_sizing="border-box",
        ),
    )
