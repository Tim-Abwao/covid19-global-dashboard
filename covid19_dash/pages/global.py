import dash
from dash import Input, Output, callback, dcc, html
from plotly.graph_objects import Figure

from covid19_dash import plotting
from covid19_dash.data import load_30_day_diff, load_latest_day_data

dash.register_page(__name__, path="/", title="COVID-19 Dashboard")

PLOT_CONFIG = {"displayModeBar": False}

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
                                id="global-choropleth-map", config=PLOT_CONFIG
                            ),
                        ),
                    ],
                ),
                html.Div(
                    className="page-link",
                    children=[
                        dcc.Link(
                            "Compare Countries",
                            href="/compare-countries",
                            refresh=True,
                        ),
                        dcc.Link(
                            "View Data", href="/raw-values", refresh=True
                        ),
                    ],
                ),
            ],
        ),
    ],
)


@callback(Output("totals", "children"), Input("column-selector", "value"))
def plot_metrics(category: str) -> list:
    """Create a card with total cases, spark-lines of new cases & deaths, and
    a gauge chart of people fully vaccinated.

    Args:
        category (str): The info to plot.

    Returns:
        list: A list of metric graphs.
    """
    latest_data = load_latest_day_data()
    daily_diff = load_30_day_diff()

    # Plot global metrics
    total_cases = plotting.plot_value(
        current_value=latest_data["Total Cases"].sum(),
        delta=daily_diff["Confirmed"].iloc[-1],
        title="Total Cases",
        color="#f77",
    )
    new_cases_sparkline = plotting.plot_spark_line(
        daily_diff["Confirmed"], color="#bbf", title="New Cases"
    )
    new_deaths = plotting.plot_spark_line(
        daily_diff["Deaths"], color="#aaa", title="Deaths"
    )
    vaccination_gauge = plotting.plot_gauge_chart(
        value=latest_data["People Fully Vaccinated"].sum(),
        reference=latest_data["Population"].sum(),
        title="People Fully Vaccinated",
        color="#7b7",
    )
    totals = [
        dcc.Loading(
            dcc.Graph(figure=graph, config=PLOT_CONFIG), color="steelblue"
        )
        for graph in [
            total_cases,
            new_cases_sparkline,
            new_deaths,
            vaccination_gauge,
        ]
    ]
    return totals


@callback(
    Output("global-choropleth-map", "figure"),
    Input("column-selector", "value"),
)
def plot_map(category: str) -> tuple[list, Figure]:
    """Create a choropleth map showing `category`s distribution globally.

    Args:
        category (str): The info to plot.

    Returns:
        plotly.graph_objs._figure.Figure: A choropleth map.
    """
    latest_data = load_latest_day_data()
    data_date = latest_data["Last Updated Date"].max().strftime("%A, %b %d %Y")

    # Negative and null values in the size parameter raise a ValueError
    latest_data[category] = latest_data[category].clip(lower=0).fillna(0)

    return plotting.plot_global_map(
        latest_data, category=category, date=data_date
    )
