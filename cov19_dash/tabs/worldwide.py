import plotly.express as px
from cov19_dash.dash_app import app
from cov19_dash.data import load_latest_day_data
from dash import dcc, html
from dash.dependencies import Input, Output
from plotly.graph_objects import Figure

layout = html.Div(
    className="global-container",
    children=[
        # Global totals
        html.Div(
            id="totals-sidebar",
            children=[html.Div(id="totals", className="totals-container")],
        ),
        # Global geo-scatterplot
        html.Div(
            children=[
                # Geo-scatterplot category selector
                dcc.Dropdown(
                    id="column-selector",
                    options=[
                        {"label": col, "value": col}
                        for col in [
                            "Total Cases",
                            "New Cases",
                            "Total Deaths",
                            "People Fully Vaccinated",
                            "Total Vaccinations",
                            "Hospital Beds Per Thousand",
                            "Aged 65 Older",
                            "Population Density",
                        ]
                    ],
                    value="New Cases",
                    clearable=False,
                    placeholder="Select category",
                    searchable=False,
                    style={"maxWidth": 700},
                ),
                # Display geo-scatterplot
                html.Div(
                    className="global-bubble-map",
                    children=[
                        dcc.Loading(
                            id="refresh-geoscatterplot",
                            color="steelblue",
                            children=dcc.Graph(id="global-bubble-map"),
                        ),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(
    [Output("totals", "children"), Output("global-bubble-map", "figure")],
    Input("column-selector", "value"),
)
def plot_global_bubble_map(category: str) -> tuple[list, Figure]:
    """Create a geo-scatterplot of case totals.

    Parameters
    ----------
    category : str
        The information (column) to plot.

    Returns
    -------
    totals : list
        Global metrics.
    global-bubble-map : plotly.graph_objs._figure.Figure
        A geo-scatterplot with values of the specified category.
    """
    data = load_latest_day_data()
    data_date = data["Last Updated Date"].max().strftime("%A, %b %d %Y")

    # Prepare totals content
    totals = (
        data[
            [
                "Total Cases",
                "New Cases",
                "Total Deaths",
                "People Fully Vaccinated",
            ]
        ]
        .sum()
        .items()
    )
    totals_color_map = {
        "Total Cases": "#4da6ff",
        "New Cases": "#ef553b",
        "Total Deaths": "#5c615f",
        "People Fully Vaccinated": "#00cc0096",
    }
    totals_content = sum(
        [
            (
                html.H2(col),
                html.H1(
                    f"{value:,.0f}", style={"color": totals_color_map[col]}
                ),
            )
            for col, value in totals
        ],
        start=(),
    )

    # Negative and null values in the size parameter raise a ValueError
    data[category] = data[category].clip(lower=0).fillna(0)

    # Plot geo-scatterplot
    geo_scatterplot = px.scatter_geo(
        data,
        locations="Iso Code",
        locationmode="ISO-3",
        color=category,
        size=category,
        size_max=40,
        hover_name="Location",
        color_continuous_scale=["#00334d", "#ffff77"],
        custom_data=[category],
        title=f"<i>{category}</i> as at {data_date}",
    )
    geo_scatterplot.update_geos(
        bgcolor="#f0ffff",
        showcountries=True,
        countrycolor="#72a0c1",
        showframe=False,
        coastlinecolor="skyblue",
    )
    geo_scatterplot.update_layout(paper_bgcolor="#f0ffff")
    geo_scatterplot.update_traces(
        hovertemplate=(
            f"<b>%{{hovertext}}</b><br>{category}: %{{customdata[0]:,}}"
        )
    )

    return totals_content, geo_scatterplot
