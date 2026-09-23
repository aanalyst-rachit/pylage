from pylage import Chart, column, run
from pylage.ENGINE.components.chart import Chart

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


# ============================================================
# 1. LINE CHART
# ============================================================
line_fig = go.Figure()

line_fig.add_trace(
    go.Scatter(
        x=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        y=[120, 150, 135, 180, 210, 240],
        mode="lines+markers",
        name="Sales",
    )
)

line_fig.update_layout(
    title="1. Line Chart",
    xaxis_title="Month",
    yaxis_title="Sales",
)


# ============================================================
# 2. BAR CHART
# ============================================================
bar_fig = go.Figure()

bar_fig.add_trace(
    go.Bar(
        x=["Python", "JavaScript", "Go", "Rust"],
        y=[82, 76, 61, 48],
        name="Popularity",
    )
)

bar_fig.update_layout(
    title="2. Bar Chart",
    xaxis_title="Language",
    yaxis_title="Score",
)


# ============================================================
# 3. MULTI-SERIES BAR
# ============================================================
multi_bar_fig = go.Figure()

multi_bar_fig.add_trace(
    go.Bar(
        x=["Q1", "Q2", "Q3", "Q4"],
        y=[100, 130, 160, 190],
        name="Product A",
    )
)

multi_bar_fig.add_trace(
    go.Bar(
        x=["Q1", "Q2", "Q3", "Q4"],
        y=[80, 110, 140, 170],
        name="Product B",
    )
)

multi_bar_fig.update_layout(
    title="3. Multi-Series Bar",
    barmode="group",
)


# ============================================================
# 4. STACKED BAR
# ============================================================
stacked_bar_fig = go.Figure()

stacked_bar_fig.add_trace(
    go.Bar(
        x=["Q1", "Q2", "Q3", "Q4"],
        y=[40, 50, 60, 70],
        name="New",
    )
)

stacked_bar_fig.add_trace(
    go.Bar(
        x=["Q1", "Q2", "Q3", "Q4"],
        y=[60, 70, 80, 90],
        name="Returning",
    )
)

stacked_bar_fig.update_layout(
    title="4. Stacked Bar",
    barmode="stack",
)


# ============================================================
# 5. SCATTER
# ============================================================
scatter_fig = go.Figure()

scatter_fig.add_trace(
    go.Scatter(
        x=[10, 20, 30, 40, 50, 60],
        y=[15, 25, 22, 40, 45, 58],
        mode="markers",
        marker={"size": 12},
        name="Observations",
    )
)

scatter_fig.update_layout(
    title="5. Scatter Plot",
    xaxis_title="X",
    yaxis_title="Y",
)


# ============================================================
# 6. BUBBLE CHART
# ============================================================
bubble_fig = go.Figure()

bubble_fig.add_trace(
    go.Scatter(
        x=[10, 20, 30, 40, 50],
        y=[20, 35, 30, 55, 70],
        mode="markers",
        marker={
            "size": [15, 30, 45, 60, 80],
        },
        text=["A", "B", "C", "D", "E"],
        name="Companies",
    )
)

bubble_fig.update_layout(
    title="6. Bubble Chart",
    xaxis_title="Growth",
    yaxis_title="Revenue",
)


# ============================================================
# 7. PIE
# ============================================================
pie_fig = go.Figure(
    data=[
        go.Pie(
            labels=["Python", "JavaScript", "Go", "Rust"],
            values=[40, 30, 20, 10],
            hole=0,
        )
    ]
)

pie_fig.update_layout(title="7. Pie Chart")


# ============================================================
# 8. DONUT
# ============================================================
donut_fig = go.Figure(
    data=[
        go.Pie(
            labels=["Product", "Services", "Ads", "Other"],
            values=[45, 25, 20, 10],
            hole=0.55,
        )
    ]
)

donut_fig.update_layout(title="8. Donut Chart")


# ============================================================
# 9. AREA CHART
# ============================================================
area_fig = go.Figure()

area_fig.add_trace(
    go.Scatter(
        x=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        y=[10, 20, 18, 30, 42, 50],
        fill="tozeroy",
        mode="lines",
        name="Traffic",
    )
)

area_fig.update_layout(title="9. Area Chart")


# ============================================================
# 10. MULTI-SERIES AREA
# ============================================================
multi_area_fig = go.Figure()

multi_area_fig.add_trace(
    go.Scatter(
        x=["Jan", "Feb", "Mar", "Apr", "May"],
        y=[10, 20, 30, 40, 50],
        stackgroup="one",
        name="Desktop",
    )
)

multi_area_fig.add_trace(
    go.Scatter(
        x=["Jan", "Feb", "Mar", "Apr", "May"],
        y=[20, 25, 30, 35, 40],
        stackgroup="one",
        name="Mobile",
    )
)

multi_area_fig.update_layout(title="10. Stacked Area")


# ============================================================
# 11. HISTOGRAM
# ============================================================
histogram_fig = go.Figure()

histogram_fig.add_trace(
    go.Histogram(
        x=[
            12, 15, 16, 18, 18, 20, 21, 22, 23, 23,
            24, 25, 26, 27, 28, 28, 30, 31, 33, 35,
        ],
        name="Values",
    )
)

histogram_fig.update_layout(
    title="11. Histogram",
    xaxis_title="Value",
    yaxis_title="Frequency",
)


# ============================================================
# 12. BOX PLOT
# ============================================================
box_fig = go.Figure()

box_fig.add_trace(
    go.Box(
        y=[12, 15, 16, 18, 18, 20, 21, 22, 23, 25, 27, 35],
        name="Dataset A",
    )
)

box_fig.add_trace(
    go.Box(
        y=[10, 13, 15, 17, 20, 21, 24, 25, 29, 32],
        name="Dataset B",
    )
)

box_fig.update_layout(title="12. Box Plot")


# ============================================================
# 13. VIOLIN
# ============================================================
violin_fig = go.Figure()

violin_fig.add_trace(
    go.Violin(
        y=[12, 15, 16, 18, 18, 20, 21, 22, 23, 25, 27, 35],
        name="Distribution",
        box_visible=True,
        meanline_visible=True,
    )
)

violin_fig.update_layout(title="13. Violin Plot")


# ============================================================
# 14. HEATMAP
# ============================================================
heatmap_fig = go.Figure(
    data=[
        go.Heatmap(
            z=[
                [10, 20, 30, 40],
                [20, 30, 40, 50],
                [30, 40, 50, 60],
                [40, 50, 60, 70],
            ],
            x=["A", "B", "C", "D"],
            y=["Row 1", "Row 2", "Row 3", "Row 4"],
        )
    ]
)

heatmap_fig.update_layout(title="14. Heatmap")


# ============================================================
# 15. CONTOUR
# ============================================================
contour_fig = go.Figure(
    data=[
        go.Contour(
            z=[
                [10, 20, 30, 40],
                [20, 30, 40, 50],
                [30, 40, 50, 60],
                [40, 50, 60, 70],
            ]
        )
    ]
)

contour_fig.update_layout(title="15. Contour Plot")


# ============================================================
# 16. CANDLESTICK
# ============================================================
candlestick_fig = go.Figure()

candlestick_fig.add_trace(
    go.Candlestick(
        x=["Mon", "Tue", "Wed", "Thu", "Fri"],
        open=[100, 110, 108, 115, 120],
        high=[115, 118, 120, 125, 130],
        low=[95, 105, 104, 110, 115],
        close=[110, 108, 115, 120, 128],
        name="Price",
    )
)

candlestick_fig.update_layout(
    title="16. Candlestick Chart",
    xaxis_title="Day",
    yaxis_title="Price",
)


# ============================================================
# 17. OHLC
# ============================================================
ohlc_fig = go.Figure()

ohlc_fig.add_trace(
    go.Ohlc(
        x=["Mon", "Tue", "Wed", "Thu", "Fri"],
        open=[100, 110, 108, 115, 120],
        high=[115, 118, 120, 125, 130],
        low=[95, 105, 104, 110, 115],
        close=[110, 108, 115, 120, 128],
        name="OHLC",
    )
)

ohlc_fig.update_layout(title="17. OHLC Chart")


# ============================================================
# 18. 3D SCATTER
# ============================================================
scatter3d_fig = go.Figure()

scatter3d_fig.add_trace(
    go.Scatter3d(
        x=[1, 2, 3, 4, 5],
        y=[5, 4, 3, 2, 1],
        z=[2, 4, 1, 5, 3],
        mode="markers",
        marker={"size": 8},
        name="3D Points",
    )
)

scatter3d_fig.update_layout(
    title="18. 3D Scatter",
    scene={
        "xaxis_title": "X",
        "yaxis_title": "Y",
        "zaxis_title": "Z",
    },
)


# ============================================================
# 19. 3D SURFACE
# ============================================================
surface_fig = go.Figure(
    data=[
        go.Surface(
            z=[
                [1, 2, 3, 4],
                [2, 4, 6, 8],
                [3, 6, 9, 12],
                [4, 8, 12, 16],
            ]
        )
    ]
)

surface_fig.update_layout(
    title="19. 3D Surface",
    scene={
        "xaxis_title": "X",
        "yaxis_title": "Y",
        "zaxis_title": "Z",
    },
)


# ============================================================
# 20. 3D MESH
# ============================================================
mesh_fig = go.Figure()

mesh_fig.add_trace(
    go.Mesh3d(
        x=[0, 1, 0, 0],
        y=[0, 0, 1, 0],
        z=[0, 0, 0, 1],
        alphahull=5,
        opacity=0.8,
        name="Mesh",
    )
)

mesh_fig.update_layout(title="20. 3D Mesh")


# ============================================================
# 21. POLAR / RADAR
# ============================================================
polar_fig = go.Figure()

polar_fig.add_trace(
    go.Scatterpolar(
        r=[80, 90, 70, 85, 95],
        theta=["Speed", "Power", "Defense", "Skill", "Stamina"],
        fill="toself",
        name="Player",
    )
)

polar_fig.update_layout(
    title="21. Polar / Radar Chart",
    polar={"radialaxis": {"visible": True}},
)


# ============================================================
# 22. FUNNEL
# ============================================================
funnel_fig = go.Figure()

funnel_fig.add_trace(
    go.Funnel(
        y=["Visitors", "Signups", "Trials", "Customers"],
        x=[10000, 5000, 2500, 1000],
        name="Conversion",
    )
)

funnel_fig.update_layout(title="22. Funnel Chart")


# ============================================================
# 23. WATERFALL
# ============================================================
waterfall_fig = go.Figure()

waterfall_fig.add_trace(
    go.Waterfall(
        x=["Start", "Sales", "Costs", "Marketing", "End"],
        y=[100, 50, -30, -10, 0],
        measure=["absolute", "relative", "relative", "relative", "total"],
        name="Profit",
    )
)

waterfall_fig.update_layout(title="23. Waterfall Chart")


# ============================================================
# 24. SUNBURST
# ============================================================
sunburst_fig = go.Figure(
    go.Sunburst(
        labels=[
            "All",
            "Technology",
            "Services",
            "Python",
            "JavaScript",
            "Consulting",
            "Support",
        ],
        parents=[
            "",
            "All",
            "All",
            "Technology",
            "Technology",
            "Services",
            "Services",
        ],
        values=[100, 60, 40, 35, 25, 25, 15],
    )
)

sunburst_fig.update_layout(title="24. Sunburst")


# ============================================================
# 25. TREEMAP
# ============================================================
treemap_fig = go.Figure(
    go.Treemap(
        labels=[
            "All",
            "Technology",
            "Services",
            "Python",
            "JavaScript",
            "Consulting",
            "Support",
        ],
        parents=[
            "",
            "All",
            "All",
            "Technology",
            "Technology",
            "Services",
            "Services",
        ],
        values=[100, 60, 40, 35, 25, 25, 15],
    )
)

treemap_fig.update_layout(title="25. Treemap")


# ============================================================
# 26. PARALLEL COORDINATES
# ============================================================
parallel_fig = go.Figure(
    data=[
        go.Parcoords(
            dimensions=[
                {"label": "A", "values": [1, 2, 3, 4]},
                {"label": "B", "values": [10, 20, 15, 30]},
                {"label": "C", "values": [100, 80, 90, 70]},
            ]
        )
    ]
)

parallel_fig.update_layout(title="26. Parallel Coordinates")


# ============================================================
# 27. SUBPLOTS / DASHBOARD
# ============================================================
dashboard_fig = make_subplots(
    rows=2,
    cols=2,
    specs=[
        [{"type": "xy"}, {"type": "xy"}],
        [{"type": "xy"}, {"type": "domain"}],
    ],
    subplot_titles=(
        "Revenue",
        "Users",
        "Distribution",
        "Categories",
    ),
)

dashboard_fig.add_trace(
    go.Scatter(
        x=["Jan", "Feb", "Mar", "Apr"],
        y=[100, 130, 160, 200],
        name="Revenue",
    ),
    row=1,
    col=1,
)

dashboard_fig.add_trace(
    go.Bar(
        x=["Jan", "Feb", "Mar", "Apr"],
        y=[20, 30, 45, 60],
        name="Users",
    ),
    row=1,
    col=2,
)

dashboard_fig.add_trace(
    go.Histogram(
        x=[1, 2, 2, 3, 3, 3, 4, 4, 5],
        name="Distribution",
    ),
    row=2,
    col=1,
)

dashboard_fig.add_trace(
    go.Pie(
        labels=["A", "B", "C"],
        values=[40, 35, 25],
        name="Categories",
    ),
    row=2,
    col=2,
)

dashboard_fig.update_layout(
    title="27. Multi-Chart Dashboard / Subplots",
    height=800,
)


# ============================================================
# 28. PLOTLY EXPRESS
# ============================================================
px_fig = px.scatter(
    x=[10, 20, 30, 40, 50],
    y=[15, 25, 35, 45, 60],
    size=[10, 20, 30, 40, 50],
    title="28. Plotly Express Chart",
)


# ============================================================
# 29. ANIMATION / FRAMES
# ============================================================
animated_fig = go.Figure(
    data=[
        go.Scatter(
            x=[1, 2, 3],
            y=[1, 2, 1],
            mode="markers+lines",
            name="Frame Data",
        )
    ],
    frames=[
        go.Frame(
            data=[
                go.Scatter(
                    x=[1, 2, 3],
                    y=[2, 3, 2],
                )
            ],
            name="frame1",
        ),
        go.Frame(
            data=[
                go.Scatter(
                    x=[1, 2, 3],
                    y=[3, 1, 3],
                )
            ],
            name="frame2",
        ),
    ],
)

animated_fig.update_layout(
    title="29. Animation / Frames",
)


# ============================================================
# PYLAGE PAGE
# ============================================================
def page():
    return column(
        Chart(line_fig, height=400),
        Chart(bar_fig, height=400),
        Chart(multi_bar_fig, height=400),
        Chart(stacked_bar_fig, height=400),
        Chart(scatter_fig, height=400),
        Chart(bubble_fig, height=400),
        Chart(pie_fig, height=400),
        Chart(donut_fig, height=400),
        Chart(area_fig, height=400),
        Chart(multi_area_fig, height=400),
        Chart(histogram_fig, height=400),
        Chart(box_fig, height=400),
        Chart(violin_fig, height=400),
        Chart(heatmap_fig, height=400),
        Chart(contour_fig, height=400),
        Chart(candlestick_fig, height=500),
        Chart(ohlc_fig, height=500),
        Chart(scatter3d_fig, height=500),
        Chart(surface_fig, height=500),
        Chart(mesh_fig, height=500),
        Chart(polar_fig, height=500),
        Chart(funnel_fig, height=500),
        Chart(waterfall_fig, height=500),
        Chart(sunburst_fig, height=500),
        Chart(treemap_fig, height=500),
        Chart(parallel_fig, height=500),
        Chart(dashboard_fig, height=800),
        Chart(px_fig, height=500),
        Chart(animated_fig, height=500),
    )


if __name__ == "__main__":
    run(page(), serve=True)
