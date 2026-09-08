import pylage as pl


def get_app():

    return pl.column(

        pl.heading(
            "pl.heading — Default",
        ),

        pl.heading(
            "pl.heading — Large",
            style=pl.style(
                font_size="2.5rem",
                font_weight="700",
                color="#0f172a",
            ),
        ),

        pl.heading(
            "pl.heading — Medium",
            style=pl.style(
                font_size="2rem",
                font_weight="600",
                color="#1e293b",
            ),
        ),

        pl.heading(
            "pl.heading — Small",
            style=pl.style(
                font_size="1.5rem",
                font_weight="600",
                color="#334155",
            ),
        ),

        pl.heading(
            "pl.heading — Custom Font",
            style=pl.style(
                font_size="2rem",
                font_family="Arial",
                font_weight="700",
                color="#2563eb",
            ),
        ),

        pl.heading(
            "pl.heading — Center",
            style=pl.style(
                font_size="2rem",
                font_weight="700",
                text_align="center",
                color="#7c3aed",
                padding="1rem",
                background_color="#f5f3ff",
            ),
        ),

        pl.heading(
            "pl.heading — With Spacing",
            style=pl.style(
                font_size="1.75rem",
                font_weight="700",
                margin="2rem",
                padding="1rem",
                color="#047857",
                background_color="#ecfdf5",
                border="1px solid #a7f3d0",
                border_radius="0.5rem",
            ),
        ),

        pl.heading(
            "pl.heading — Full Width",
            style=pl.style(
                width="100%",
                font_size="2rem",
                font_weight="700",
                text_align="center",
                padding="1rem",
                background_color="#eff6ff",
                color="#1d4ed8",
                box_sizing="border-box",
            ),
        ),

        pl.heading(
            "pl.heading — Line Height",
            style=pl.style(
                font_size="2rem",
                font_weight="700",
                line_height="1.5",
                color="#be123c",
            ),
        ),

        pl.heading(
            "pl.heading — Shadow",
            style=pl.style(
                font_size="2rem",
                font_weight="700",
                color="#111827",
                box_shadow="0 2px 6px rgba(0,0,0,0.15)",
                padding="1rem",
            ),
        ),

        style=pl.style(
            width="100%",
            min_height="100vh",
            padding="2rem",
            gap="1rem",
            background_color="#f8fafc",
            color="#0f172a",
            box_sizing="border-box",
        ),
    )
