import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from cov19_dash.dash_app import app
from cov19_dash.data import load_latest_day_data, load_time_series_data
from dash.dependencies import Input, Output
from plotly.graph_objects import Figure


time_series_data = load_time_series_data()
latest_day_data = load_latest_day_data()

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
                            children=dcc.Graph(id="line-plot"),
                            color="steelblue",
                        ),
                    ]
                ),
            ],
        ),
        # Country pie-charts
        html.Div(className="pie-charts", id="pie-charts"),
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

    lineplot = px.line(data, x="Date", y=category, color="Country/Region")
    lineplot.update_layout(paper_bgcolor="#f0ffff", plot_bgcolor="#f0ffff")
    lineplot.update_traces(hovertemplate="<b>%{x}</b><br>%{y:,}")
    lineplot.update_xaxes(fixedrange=True)
    lineplot.update_yaxes(fixedrange=True)

    return lineplot


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
    pie-charts : list[Figure]
        Country comparisons.
    """
    if countries == []:  # If no country is selected
        countries = ["Kenya", "Uganda", "Tanzania"]

    data = latest_day_data.set_index("Location").loc[countries]

    pie_charts = []
    for metric in (
        "Total Cases Per Million",
        "Total Deaths Per Million",
        "People Vaccinated Per Hundred",
        "People Fully Vaccinated Per Hundred",
        "Hospital Beds Per Thousand",
        "Population Density",
    ):
        fig = px.pie(
            values=data[metric],
            names=countries,
            color=countries,
            title=(f"{metric.replace('_', ' ').title()}"),
            hole=0.4,
        )
        fig.update_layout(paper_bgcolor="#f0ffff", plot_bgcolor="#f0ffff")
        fig.update_traces(
            hovertemplate="<b>%{label}:</b> %{value:,}<extra></extra>"
        )
        pie_div = html.Div(dcc.Graph(id=f"{metric}-pie-chart", figure=fig))
        pie_charts.append(pie_div)

    return pie_charts
