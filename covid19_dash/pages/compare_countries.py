import dash
from covid19_dash import plotting
from covid19_dash.data import load_latest_day_data, load_time_series_data
from dash import Input, Output, callback, dcc, html
from plotly.graph_objects import Figure

dash.register_page(__name__, title="Compare Countries")

time_series_data = load_time_series_data()
latest_day_data = load_latest_day_data()

countries_in_ts = set(time_series_data["Country/Region"].unique())
countries_in_latest = set(latest_day_data["Location"].unique())
countries = sorted(countries_in_ts.intersection(countries_in_latest))

EAST_AFRICA = [
    "Burundi",
    "Democratic Republic of Congo",
    "Kenya",
    "Rwanda",
    "South Sudan",
    "Tanzania",
    "Uganda",
]
PLOT_CONFIG = {"displayModeBar": False}

layout = html.Div(
    [
        # Trend (line-plots)
        html.Div(
            className="line-plots",
            children=[
                html.Div(
                    children=[
                        # Select country
                        dcc.Dropdown(
                            id="countries",
                            options=countries,
                            multi=True,
                            clearable=False,
                            persistence=True,
                            placeholder="Select a Country",
                            value=EAST_AFRICA,
                        ),
                        # Select category
                        dcc.RadioItems(
                            id="info-category",
                            options=[
                                {"label": category, "value": category}
                                for category in [
                                    "Confirmed",
                                    "Deaths",
                                ]
                            ],
                            value="Confirmed",
                        ),
                        # Line-plot
                        dcc.Loading(
                            id="line-plot-container",
                            children=dcc.Graph(
                                id="line-plot", config=PLOT_CONFIG
                            ),
                            color="steelblue",
                        ),
                    ]
                ),
            ],
        ),
        # Country column-charts
        html.Div(className="column-charts", id="column-charts"),
        html.Div(
            className="page-link",
            children=[
                dcc.Link("Global Dashboard", href="/"),
                dcc.Link("View Data", href="/raw-values"),
            ],
        ),
    ]
)


@callback(
    Output("line-plot", "figure"),
    [Input("countries", "value"), Input("info-category", "value")],
)
def plot_lineplots(countries: list, category: str) -> Figure:
    """Get a line-plot of `category` values for various countries.

    Args:
        countries (list): Selected countries.
        category (str): "Confirmed" or "Deaths".

    Returns:
        plotly.graph_objs._figure.Figure: Comparative line-plot.
    """
    if not countries:  # If no country is selected
        countries = EAST_AFRICA

    data = time_series_data.query("`Country/Region` in @countries")
    return plotting.plot_lines(data, category)


@callback(
    Output("column-charts", "children"),
    Input("countries", "value"),
)
def plot_column_charts(countries: list) -> list[Figure]:
    """Get a barplot, and column-charts for each of the supplied countries.

    Args:
        countries (list): Selected countries.

    Returns:
        list[Figure]: Comparative graphs.
    """
    if countries == []:  # If no country is selected
        countries = ["Kenya", "Uganda", "Tanzania"]

    data = latest_day_data.query("Location in @countries")
    column_charts = [
        html.Div(
            dcc.Graph(
                id=f"{metric}-column-chart",
                figure=plotting.plot_column_chart(data, metric),
                config=PLOT_CONFIG,
                className="a-column-chart",
            )
        )
        for metric in (
            "Total Cases",
            "Total Cases Per Million",
            "Total Deaths",
            "Total Deaths Per Million",
            "People Fully Vaccinated",
            "People Fully Vaccinated Per Hundred",
            "Hospital Beds Per Thousand",
            "Population Density",
        )
    ]
    return column_charts
