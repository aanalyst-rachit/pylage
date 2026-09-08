import pylage as pl


def get_app():

    return pl.column(

        # =========================================================
        # TEXT — BASIC
        # =========================================================
        pl.text(
            "TEXT — Basic",
            style=pl.style(
                font_size="28px",
                font_weight="700",
                color="#0f172a",
                margin_bottom="10px",
            ),
        ),

        pl.text(
            "This is a normal pl.text component.",
            style=pl.style(
                color="#334155",
                font_size="16px",
            ),
        ),

        # =========================================================
        # FONT SIZE
        # =========================================================
        pl.text(
            "Font Size: 12px",
            style=pl.style(
                font_size="12px",
                color="#475569",
            ),
        ),

        pl.text(
            "Font Size: 20px",
            style=pl.style(
                font_size="20px",
                color="#475569",
            ),
        ),

        pl.text(
            "Font Size: 32px",
            style=pl.style(
                font_size="32px",
                color="#475569",
            ),
        ),

        # =========================================================
        # FONT WEIGHT
        # =========================================================
        pl.text(
            "Font Weight: 400 — Normal",
            style=pl.style(
                font_weight="400",
                font_size="18px",
            ),
        ),

        pl.text(
            "Font Weight: 600 — Semi Bold",
            style=pl.style(
                font_weight="600",
                font_size="18px",
            ),
        ),

        pl.text(
            "Font Weight: 700 — Bold",
            style=pl.style(
                font_weight="700",
                font_size="18px",
            ),
        ),

        # =========================================================
        # FONT FAMILY
        # =========================================================
        pl.text(
            "Font Family: Arial",
            style=pl.style(
                font_family="Arial",
                font_size="20px",
            ),
        ),

        pl.text(
            "Font Family: Georgia",
            style=pl.style(
                font_family="Georgia",
                font_size="20px",
            ),
        ),

        pl.text(
            "Font Family: monospace",
            style=pl.style(
                font_family="monospace",
                font_size="20px",
            ),
        ),

        # =========================================================
        # COLOR
        # =========================================================
        pl.text(
            "pl.text Color",
            style=pl.style(
                color="#2563eb",
                font_size="22px",
                font_weight="700",
            ),
        ),

        pl.text(
            "Different pl.text Color",
            style=pl.style(
                color="#dc2626",
                font_size="22px",
                font_weight="700",
            ),
        ),

        # =========================================================
        # BACKGROUND
        # =========================================================
        pl.text(
            "pl.text with Background",
            style=pl.style(
                background_color="#dbeafe",
                color="#1e40af",
                padding="10px",
                font_weight="700",
            ),
        ),

        # =========================================================
        # TEXT ALIGN
        # =========================================================
        pl.text(
            "Left Aligned pl.text",
            style=pl.style(
                width="100%",
                text_align="left",
                font_size="18px",
            ),
        ),

        pl.text(
            "Center Aligned pl.text",
            style=pl.style(
                width="100%",
                text_align="center",
                font_size="18px",
            ),
        ),

        pl.text(
            "Right Aligned pl.text",
            style=pl.style(
                width="100%",
                text_align="right",
                font_size="18px",
            ),
        ),

        # =========================================================
        # LINE HEIGHT
        # =========================================================
        pl.text(
            "Line Height Demo — This is a longer piece of text "
            "so that we can visually inspect how line-height "
            "changes the spacing between lines.",
            style=pl.style(
                width="500px",
                font_size="18px",
                line_height="2",
            ),
        ),

        # =========================================================
        # PADDING
        # =========================================================
        pl.text(
            "pl.text with Padding",
            style=pl.style(
                background_color="#fef3c7",
                color="#92400e",
                padding="20px",
                font_weight="700",
            ),
        ),

        # =========================================================
        # MARGIN
        # =========================================================
        pl.text(
            "pl.text with Margin",
            style=pl.style(
                background_color="#dcfce7",
                color="#166534",
                padding="10px",
                margin="20px",
                font_weight="700",
            ),
        ),

        # =========================================================
        # BORDER
        # =========================================================
        pl.text(
            "pl.text with Border",
            style=pl.style(
                border="1px solid #94a3b8",
                padding="12px",
                border_radius="8px",
                color="#0f172a",
            ),
        ),

        # =========================================================
        # BORDER RADIUS
        # =========================================================
        pl.text(
            "Rounded pl.text Box",
            style=pl.style(
                background_color="#ede9fe",
                color="#5b21b6",
                padding="12px 20px",
                border_radius="20px",
                font_weight="700",
            ),
        ),

        # =========================================================
        # BOX SHADOW
        # =========================================================
        pl.text(
            "pl.text Box with Shadow",
            style=pl.style(
                background_color="#ffffff",
                color="#0f172a",
                padding="15px",
                border_radius="8px",
                box_shadow="0 4px 10px rgba(0,0,0,0.15)",
            ),
        ),

        # =========================================================
        # OPACITY
        # =========================================================
        pl.text(
            "Opacity 100%",
            style=pl.style(
                opacity=1,
                font_size="18px",
            ),
        ),

        pl.text(
            "Opacity 50%",
            style=pl.style(
                opacity=0.5,
                font_size="18px",
            ),
        ),

        # =========================================================
        # WIDTH
        # =========================================================
        pl.text(
            "Fixed Width pl.text",
            style=pl.style(
                width="300px",
                background_color="#e0f2fe",
                padding="10px",
            ),
        ),

        # =========================================================
        # OVERFLOW
        # =========================================================
        pl.text(
            "Overflow demonstration — this is intentionally a "
            "very long text string to inspect overflow behaviour.",
            style=pl.style(
                width="250px",
                overflow="hidden",
                background_color="#f1f5f9",
                padding="10px",
            ),
        ),

        # =========================================================
        # CURSOR
        # =========================================================
        pl.text(
            "Cursor: pointer",
            style=pl.style(
                cursor="pointer",
                color="#2563eb",
                font_weight="700",
            ),
        ),

        # =========================================================
        # COMBINED REAL-WORLD TEXT
        # =========================================================
        pl.text(
            "Dashboard Title",
            style=pl.style(
                font_size="30px",
                font_weight="700",
                font_family="Arial",
                color="#0f172a",
                margin_bottom="8px",
            ),
        ),

        pl.text(
            "Manage your application, users and analytics "
            "from one place.",
            style=pl.style(
                font_size="16px",
                font_weight="400",
                color="#64748b",
                line_height="1.6",
                max_width="600px",
            ),
        ),

        style=pl.style(
            width="100%",
            min_height="100vh",
            padding="30px",
            background_color="#f8fafc",
            color="#0f172a",
            display="flex",
            flex_direction="column",
            gap="16px",
            box_sizing="border-box",
        ),
    )
