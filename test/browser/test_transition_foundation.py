import pylage as pl
from pylage.ENGINE.core.renderer import render


def test_transition_foundation():
    app = pl.column(
        pl.input(
            placeholder="Name",
            style=pl.style(
                transition="border-color 150ms ease, box-shadow 150ms ease",
            ),
        ),
        pl.button(
            "Hover",
            variant="primary",
            style=pl.style(
                transition="background-color 200ms ease",
            ),
        ),
    )

    html = render(app)

    assert "transition:border-color 150ms ease, box-shadow 150ms ease" in html
    assert "transition:background-color 200ms ease" in html
