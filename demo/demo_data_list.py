import pylage as pl
import pylage as ps
import pylage as ui

def get_app():
    return pl.column(
        pl.heading("PyLage UI Kit — Data List", level=2),
        pl.text("Key-value summary lists for resource details, specs, and accounts."),
        pl.grid(
            ui.data_list({
                "Account": "Enterprise Cloud",
                "Subscription": ui.badge("Active", variant="success"),
                "Billing Cycle": "Monthly (Auto-renew)",
                "Renewal Date": "October 1, 2026",
            }),
            ui.data_list([
                ("Host", "api.pylage.dev"),
                ("Cluster", "us-east-4"),
                ("Uptime", "99.98%"),
                ("Health", ui.badge("Healthy", variant="success")),
            ]),
            ui.data_list({
                "Primary Region": "ap-south-1",
                "Backup Node": "ap-south-2",
                "Storage Used": "42.8 GB / 100 GB",
            }, orientation="vertical"),
            style=pl.style(
                display="grid",
                grid_template_columns="repeat(auto-fit, minmax(320px, 1fr))",
                gap="1.5rem",
                width="100%",
            ),
        ),
        gap="1.5rem",
        style=pl.style(max_width="1200px", margin="0 auto", padding="2rem"),
    )
