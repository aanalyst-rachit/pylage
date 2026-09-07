from __future__ import annotations

from pylage.ENGINE import Style
from pylage.ENGINE.core.renderer import render
from pylage.UI import dataframe


class FakeDataFrame:
    columns = ["Name", "Age"]

    def to_dict(self, orient="records"):
        assert orient == "records"
        return [
            {"Name": "Rachit", "Age": 24},
            {"Name": "Rahul", "Age": 25},
        ]


def test_ui_kit_dataframe_accepts_dataframe_like_object():
    html = render(dataframe(FakeDataFrame()))

    assert "<thead>" in html
    assert '<th class="pylage-dataframe__header" data-column-index="0">Name</th>' in html
    assert '<td class="pylage-dataframe__cell" data-column-index="0">Rachit</td>' in html
    assert 'class="pylage-dataframe"' in html


def test_ui_kit_dataframe_accepts_headers_and_rows():
    html = render(
        dataframe(
            [[1, "Rachit"], [2, "Rahul"]],
            headers=["ID", "Name"],
        )
    )

    assert '<th class="pylage-dataframe__header" data-column-index="0">ID</th>' in html
    assert '<td class="pylage-dataframe__cell" data-column-index="1">Rahul</td>' in html


def test_ui_kit_dataframe_merges_custom_style():
    html = render(
        dataframe(
            [{"Name": "Rachit"}],
            style=Style(width="80%"),
        )
    )

    assert "width:80%" in html
    assert "border:1px solid" in html


def test_ui_kit_dataframe_does_not_require_pandas():
    html = render(
        dataframe(
            [
                {"Name": "Rachit", "Score": 95},
                {"Name": "Rahul", "Score": 91},
            ]
        )
    )

    assert '<th class="pylage-dataframe__header" data-column-index="0">Name</th>' in html
    assert '<td class="pylage-dataframe__cell pylage-dataframe__cell--numeric" data-column-index="1">91</td>' in html


def test_ui_kit_dataframe_accepts_real_pandas_dataframe():
    pd = __import__("pytest").importorskip("pandas")

    df = pd.DataFrame(
        {
            "order_id": ["AG-2011-2040", "IN-2011-47883"],
            "order_date": ["2011-01-01", "2011-01-01"],
            "ship_date": ["2011-06-01", "2011-08-01"],
            "ship_mode": ["Standard Class", "Standard Class"],
            "customer_name": ["Toby Braunhardt", "Joseph Holt"],
            "segment": ["Consumer", "Consumer"],
            "state": ["Constantine", "New South Wales"],
            "country": ["Algeria", "Australia"],
            "market": ["Africa", "APAC"],
            "region": ["Africa", "Oceania"],
            "product_id": ["OFF-TEN-10000025", "OFF-SU-10000618"],
            "category": ["Office Supplies", "Office Supplies"],
            "sub_category": ["Storage", "Supplies"],
            "product_name": [
                "Tenex Lockers, Blue",
                "Acme Trimmer, High Speed",
            ],
            "sales": [408.0, 120.0],
            "quantity": [2, 3],
            "discount": [0.0, 0.1],
            "profit": [106.14, 36.036],
            "shipping_cost": [35.46, 9.72],
            "order_priority": ["Medium", "Medium"],
            "year": [2011, 2011],
        }
    )

    assert df.shape == (2, 21)

    html = render(dataframe(df))

    assert "<thead>" in html
    assert '<th class="pylage-dataframe__header" data-column-index="0">order_id</th>' in html
    assert '<th class="pylage-dataframe__header" data-column-index="13">product_name</th>' in html
    assert '<th class="pylage-dataframe__header" data-column-index="14">sales</th>' in html
    assert '<th class="pylage-dataframe__header" data-column-index="20">year</th>' in html

    # Verify actual CSV data reached the renderer.
    first_order_id = str(df.iloc[0]["order_id"])
    first_product = str(df.iloc[0]["product_name"])
    assert first_order_id in html
    assert first_product in html


def test_ui_kit_dataframe_cell_borders_are_on_by_default():
    html = render(
        dataframe(
            [{"Name": "Rachit", "Score": 95}],
        )
    )

    assert 'class="pylage-dataframe"' in html
    assert ".pylage-dataframe__grid th" in html
    assert "border-right: 1px solid #e2e8f0" in html
    assert "border-bottom: 1px solid #e2e8f0" in html


def test_ui_kit_dataframe_can_disable_cell_borders():
    html = render(
        dataframe(
            [{"Name": "Rachit", "Score": 95}],
            cell_border=False,
        )
    )

    assert (
        'class="pylage-dataframe pylage-dataframe--no-cell-border"'
        in html
    )
    assert ".pylage-dataframe--no-cell-border" in html
    assert "border-right: 0" in html
    assert "border-bottom: 0" in html


def test_ui_kit_dataframe_outer_border_remains_when_cell_borders_are_disabled():
    html = render(
        dataframe(
            [{"Name": "Rachit", "Score": 95}],
            cell_border=False,
        )
    )

    # The outer DataFrame container keeps its default border.
    assert "border:1px solid" in html

    # Cell borders are independently disabled.
    assert "border-right: 0" in html
    assert "border-bottom: 0" in html
