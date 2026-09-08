import pylage as pl
import pylage as ps

def get_app():
    return pl.column(
        ps.heading("Badge"),
        ps.text("Semantic status and category badges."),
        # pl.row me wraps karke align-items start karein
        pl.row(
            ps.badge("Default"),
            ps.badge("Primary", variant="primary"),
            ps.badge("Secondary", variant="secondary"),
            ps.badge("Success", variant="success"),
            ps.badge("Warning", variant="warning"),
            ps.badge("Danger", variant="danger"),
            ps.badge("Info", variant="info"),
            gap="0.5rem",
            wrap=True
        ),
        gap="1rem"
    )