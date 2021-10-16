from cov19_dash import plotting
from cov19_dash.dash_app import app
from cov19_dash.data import load_latest_day_data, load_time_series_data
from dash import dcc, html
from dash.dependencies import Input, Output
from plotly.graph_objects import Figure

time_series_data = load_time_series_data()
latest_day_data = load_latest_day_data()
plot_config = {"displayModeBar": False}

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
                            options=[
                                {"label": country, "value": country}
                                for country in time_series_data[
                                    "Country/Region"
                                ].unique()
                            ],
                            multi=True,
                            clearable=False,
                            persistence=True,
                            placeholder="Select a Country",
                            value=["Kenya", "Uganda", "Tanzania"],
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
                                id="line-plot", config=plot_config
                            ),
                            color="steelblue",
                        ),
                    ]
                ),
            ],
        ),
        # Country pie-charts
        html.Div(className="pie-charts", id="pie-charts"),
        html.Div(
            className="page-link",
            children=[
                dcc.Link("Global Dashboard", href="/"),
                dcc.Link("View Data", href="/data"),
            ],
        ),
    ]
)


@app.callback(
    Output("line-plot", "figure"),
    [Input("countries", "value"), Input("info-category", "value")],
)
def plot_lineplots(countries: list, category: str) -> Figure:
    """Get a lineplot of `category` values for various countries.

    Parameters
    ----------
    countries : list
        A list of country names.
    category : {"Confirmed", "Deaths"}

    Returns
    -------
    plotly.graph_objs._figure.Figure
        A comparative lineplot, with a line for each country.
    """
    if not countries:  # If no country is selected
        countries = ["Kenya", "Uganda", "Tanzania"]

    data = time_series_data.query("`Country/Region` in @countries")
    return plotting.plot_lines(data, category)


@app.callback(
    Output("pie-charts", "children"),
    Input("countries", "value"),
)
def plot_piecharts(countries) -> list[Figure]:
    """Get a barplot, and pie-charts for each of the supplied countries.

    Parameters
    ----------
    countries : list
        A list of countries to compare.

    Returns
    -------
    pie-charts : list[plotly.graph_objs._figure.Figure]
        Country comparisons.
    """
    if countries == []:  # If no country is selected
        countries = ["Kenya", "Uganda", "Tanzania"]

    data = latest_day_data.set_index("Location").loc[countries]

    pie_charts = [
        html.Div(
            dcc.Graph(
                id=f"{metric}-pie-chart",
                figure=plotting.plot_pie_chart(data, metric, countries),
                config=plot_config,
            )
        )
        for metric in (
            "Total Cases Per Million",
            "Total Deaths Per Million",
            "People Vaccinated Per Hundred",
            "People Fully Vaccinated Per Hundred",
            "Hospital Beds Per Thousand",
            "Population Density",
        )
    ]
    return pie_charts
