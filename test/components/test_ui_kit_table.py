from pylage.ENGINE import Style
from pylage.ENGINE.core.renderer import render
from pylage.UI import table


class FakeDataFrame:
    columns = ["Name", "Age"]

    def to_dict(self, orient="records"):
        assert orient == "records"
        return [
            {"Name": "Rachit", "Age": 24},
            {"Name": "Rahul", "Age": 25},
        ]


def test_ui_kit_table_renders_record_dicts():
    html = render(table([
        {"Name": "Rachit", "Age": 24},
        {"Name": "Rahul", "Age": 25},
    ]))
    assert "<thead>" in html
    assert "<th>Name</th>" in html
    assert "<td>25</td>" in html


def test_ui_kit_table_accepts_dataframe_like_object():
    html = render(table(FakeDataFrame()))
    assert "<th>Name</th>" in html
    assert "<td>Rachit</td>" in html


def test_ui_kit_table_accepts_headers_and_rows():
    html = render(table(
        [[1, "Rachit"], [2, "Rahul"]],
        headers=["ID", "Name"],
    ))
    assert "<th>ID</th>" in html
    assert "<td>Rahul</td>" in html


def test_ui_kit_table_merges_custom_style():
    html = render(table(
        [{"Name": "Rachit"}],
        style=Style(width="80%"),
    ))
    assert "width:80%" in html
    assert "border:1px solid" in html


def test_ui_kit_table_passes_props_through():
    html = render(table(
        [{"Name": "Rachit"}],
        title="Users",
        class_name="users-table",
    ))
    assert 'title="Users"' in html
    assert 'class="users-table"' in html


def test_ui_kit_table_has_default_cell_spacing_and_alignment():
    html = render(table([[1, "Rachit"]], headers=["ID", "Name"]))
    css = "".join(html.split())
    assert "th,td" in css
    assert "padding:0.75rem1rem" in css
    assert "text-align:left" in css


def test_ui_kit_table_has_default_row_dividers():
    html = render(table([[1, "Rachit"], [2, "Rahul"]], headers=["ID", "Name"]))
    css = "".join(html.split())
    assert "border-bottom:1pxsolidvar(--color-border)" in css
