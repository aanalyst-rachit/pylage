import pylage as pl


def get_app():
    page_style = pl.style(
        width="100%",
        max_width="1200px",
        margin="0 auto",
        padding="2rem",
        box_sizing="border-box",
    )

    grid_style = pl.style(
        display="grid",
        grid_template_columns="repeat(auto-fit, minmax(320px, 1fr))",
        gap="1.25rem",
        width="100%",
    )

    return pl.column(
        pl.heading(
            "PyLage UI Kit — Alert",
            level=2,
        ),

        pl.text(
            "Semantic feedback alerts using the existing PyLage Alert component.",
        ),

        pl.grid(
            pl.alert(
                "This is a default informational message.",
                variant="default",
            ),

            pl.alert(
                "Your profile was updated successfully.",
                variant="success",
            ),

            pl.alert(
                "Please review the information before continuing.",
                variant="warning",
            ),

            pl.alert(
                "Something went wrong while processing your request.",
                variant="danger",
            ),

            pl.alert(
                "An unexpected error occurred.",
                variant="error",
            ),

            pl.alert(
                "Additional information is available here.",
                variant="info",
            ),

            style=grid_style,
        ),

        pl.alert(
            pl.text("Alert with multiple children"),
            pl.text(
                "The UI Kit wrapper preserves existing PyLage components "
                "as children."
            ),
            variant="info",
            title="Component composition",
        ),

        gap="1.5rem",
        style=page_style,
    )


if __name__ == "__main__":
    pl.run(
        get_app(),
        title="PyLage Alert Manual",
        serve=True,
        host="0.0.0.0",
        port=3000,
    )
