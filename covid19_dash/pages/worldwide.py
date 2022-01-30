from covid19_dash.dash_app import app
from covid19_dash.data import load_latest_day_data, load_time_series_data
from covid19_dash import plotting
from dash import dcc, html
from dash.dependencies import Input, Output
from plotly.graph_objects import Figure


plot_config = {"displayModeBar": False}

layout = html.Div(
    className="global-dashboard",
    children=[
        # Global metrics
        html.Div(id="totals", className="metrics-container"),
        html.Div(
            className="global-map-container",
            children=[
                # Global map category selector
                html.Label("Select Category", htmlFor="column-selector"),
                dcc.Dropdown(
                    id="column-selector",
                    options=[
                        {"label": col, "value": col}
                        for col in [
                            "New Cases",
                            "Total Cases Per Million",
                            "Total Cases",
                            "Total Deaths",
                            "People Fully Vaccinated Per Hundred",
                            "People Fully Vaccinated",
                            "Total Vaccinations",
                            "Hospital Beds Per Thousand",
                            "Aged 70 Older",
                            "Diabetes Prevalence",
                            "Life Expectancy",
                        ]
                    ],
                    value="New Cases",
                    clearable=False,
                    placeholder="Select category",
                    searchable=False,
                    style={"maxWidth": 400},
                ),
                # Global choropleth map
                html.Div(
                    className="global-choropleth-map",
                    children=[
                        dcc.Loading(
                            id="refresh-choropleth-map",
                            color="steelblue",
                            children=dcc.Graph(
                                id="global-choropleth-map", config=plot_config
                            ),
                        ),
                    ],
                ),
                html.Div(
                    className="page-link",
                    children=[
                        dcc.Link(
                            "Compare Countries", href="/compare-countries"
                        ),
                        dcc.Link("View Data", href="/data"),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(
    [Output("totals", "children"), Output("global-choropleth-map", "figure")],
    Input("column-selector", "value"),
)
def plot_metrics_and_map(category: str) -> tuple[list, Figure]:
    """Create cards, spark-lines of new cases, a gauge chart of vaccinations and a
    choropleth map.

    Parameters
    ----------
    category : str
        The information (column) to plot.

    Returns
    -------
    totals : list
        Global metrics.
    global-choropleth-map : plotly.graph_objs._figure.Figure
        A choropleth map with values of the specified category.
    """
    latest_data = load_latest_day_data()
    ts_data = load_time_series_data()
    data_date = latest_data["Last Updated Date"].max().strftime("%A, %b %d %Y")

    # Plot global metrics
    total_cases = plotting.plot_value(
        latest_data["Total Cases"].sum(), title="Total Cases", color="#446"
    )
    daily_differences = ts_data.groupby("Date").sum().diff().tail(30)
    new_cases_sparkline = plotting.plot_spark_line(
        daily_differences["Confirmed"], color="#f51", title="New Cases"
    )
    new_deaths = plotting.plot_spark_line(
        daily_differences["Deaths"], color="#555", title="Deaths"
    )
    vaccination_gauge = plotting.plot_gauge_chart(
        value=latest_data["People Fully Vaccinated"].sum(),
        reference=latest_data["Population"].sum(),
        title="People Fully Vaccinated",
    )
    totals = [
        dcc.Graph(figure=total_cases, config=plot_config),
        dcc.Graph(figure=new_cases_sparkline, config=plot_config),
        dcc.Graph(figure=new_deaths, config=plot_config),
        dcc.Graph(figure=vaccination_gauge, config=plot_config),
    ]

    # Negative and null values in the size parameter raise a ValueError
    latest_data[category] = latest_data[category].clip(lower=0).fillna(0)

    # Plot choropleth map
    choropleth_map = plotting.plot_global_map(
        latest_data, category=category, date=data_date
    )

    return totals, choropleth_map
