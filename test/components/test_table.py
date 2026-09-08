from pylage.ENGINE import Table, Text
from pylage.ENGINE.core.renderer import render


class FakeDataFrame:
    columns = ["Name", "Age"]

    def to_dict(self, orient="records"):
        assert orient == "records"
        return [
            {"Name": "Rachit", "Age": 24},
            {"Name": "Rahul", "Age": 25},
        ]


def test_table_renders_as_table():
    html = render(Table())
    assert "<table" in html
    assert "</table>" in html


def test_table_renders_children():
    table = Table(Text("Row 1"), Text("Row 2"))
    html = render(table)
    assert "Row 1" in html
    assert "Row 2" in html


def test_table_supports_props():
    table = Table(class_name="data-table", title="Users")
    html = render(table)
    assert 'class="data-table"' in html
    assert 'title="Users"' in html


def test_table_renders_headers_and_rows():
    html = render(Table(
        headers=["ID", "Name"],
        data=[[1, "Rachit"], [2, "Rahul"]],
    ))
    assert "<thead>" in html
    assert "<th>ID</th>" in html
    assert "<th>Name</th>" in html
    assert "<td>1</td>" in html
    assert "<td>Rachit</td>" in html


def test_table_accepts_dataframe_like_object():
    html = render(Table(FakeDataFrame()))
    assert "<th>Name</th>" in html
    assert "<th>Age</th>" in html
    assert "<td>Rachit</td>" in html
    assert "<td>24</td>" in html


def test_table_accepts_record_dicts():
    html = render(Table([
        {"Name": "Rachit", "Age": 24},
        {"Name": "Rahul", "Age": 25},
    ]))
    assert "<th>Name</th>" in html
    assert "<th>Age</th>" in html
    assert "<td>Rahul</td>" in html


def test_table_accepts_column_mapping():
    html = render(Table({
        "Name": ["Rachit", "Rahul"],
        "Age": [24, 25],
    }))
    assert "<th>Name</th>" in html
    assert "<td>25</td>" in html


def test_table_escapes_cell_html():
    html = render(Table(
        headers=["Name"],
        data=[["<script>alert(1)</script>"]],
    ))
    assert "&lt;script&gt;" in html
    assert "<script>" not in html
