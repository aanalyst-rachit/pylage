from pathlib import Path

import pylage as pl


def test_run_public_api_compatibility(tmp_path):
    app = pl.column(
        pl.heading("Compatibility Test"),
        pl.button("Click me"),
    )

    output = pl.run(
        app,
        title="Compatibility Test",
        output=tmp_path / "compat_output" / "index.html",
        open_browser=False,
    )

    assert isinstance(output, Path)
    assert output.exists()

    html = output.read_text(encoding="utf-8")

    assert "<title>Compatibility Test</title>" in html
    assert "Compatibility Test" in html
    assert "Click me" in html
