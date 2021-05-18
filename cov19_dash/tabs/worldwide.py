import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from cov19_dash.dash_app import app
from cov19_dash.data import load_latest_day_data, load_time_series_data
from dash.dependencies import Input, Output

layout = html.Div(
    className="global-container",
    children=[
        # Global totals
        html.Div(
            id="global-sidebar",
            children=[html.Div(id="totals", className="totals-container")],
        ),
        # Global geo-scatterplot
        html.Div(
            className="global-map-container",
            children=[
                # Geo-scatterplot category selector
                dcc.RadioItems(
                    id="category-global-totals",
                    options=[
                        {"label": "Confirmed", "value": "Confirmed"},
                        {"label": "Active", "value": "Active"},
                        {"label": "Recovered", "value": "Recovered"},
                        {"label": "Deaths", "value": "Deaths"},
                    ],
                    value="Confirmed",
                ),
                # Display geo-scatterplot
                dcc.Loading(
                    id="refresh-geoscatterplot",
                    color="steelblue",
                    children=dcc.Graph(id="global-bubble-map"),
                ),
            ],
        ),
        html.Div(id="placeholder"),
        # New cases bar-plot
        html.Div(
            className="global-map-container",
            children=[
                # New case category selector
                dcc.RadioItems(
                    id="category-new-cases",
                    options=[
                        {"label": "Confirmed", "value": "Confirmed"},
                        {"label": "Active", "value": "Active"},
                        {"label": "Recovered", "value": "Recovered"},
                        {"label": "Deaths", "value": "Deaths"},
                    ],
                    value="Confirmed",
                ),
                # Display a bar-plot of new cases
                dcc.Loading(
                    id="refresh-barplot",
                    color="steelblue",
                    children=dcc.Graph(id="new-cases-barplot"),
                ),
            ],
        ),
    ],
)


@app.callback(
    [Output("totals", "children"), Output("global-bubble-map", "figure")],
    Input("category-global-totals", "value"),
)
def plot_global_bubble_map(category):
    """Create a geo-scatterplot of case totals.

    Parameters
    ----------
    category: {"Confirmed", "Recovered", "Active", "Deaths"}

    Returns
    -------
    Category totals, and a geo-scatterplot showing values of the specified
    category.
    """
    data = load_latest_day_data()
    data_date = data["Date"].max().strftime("%A, %b %-d %Y")

    # Prepare totals content
    totals = data[["Confirmed", "Recovered", "Active", "Deaths"]].sum().items()
    totals_content = html.Div(
        children=sum(
            [
                (
                    html.H2(col),
                    html.H1(f"{value:,}", id=f"{col.lower()}-total"),
                )
                for col, value in totals
            ],
            start=(),
        )
    )
    # Negative values in the size parameter raise a ValueError
    data[category] = data[category].clip(lower=0)

    # Plot geo-scatterplot
    geo_scatterplot = px.scatter_geo(
        data,
        lat="Lat",
        lon="Long",
        color=category,
        size=category,
        size_max=60,
        hover_name="Country/Region",
        color_continuous_scale=["#00334d", "#ffff77"],
        custom_data=[category],
        title=f"Global Totals <i>({category})</i> as at {data_date}",
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
        hovertemplate=f"""<b>%{{hovertext}}</b><br>\
{category}: %{{customdata[0]:,}}"""
    )

    return totals_content, geo_scatterplot


@app.callback(
    Output("new-cases-barplot", "figure"), Input("category-new-cases", "value")
)
def plot_daily_new_cases(category):
    """Create a bar-plot of daily new cases.

    Parameters
    ----------
    category: {"Confirmed", "Recovered", "Active", "Deaths"}

    Returns
    -------
    A bar-plot of new cases for the specified category.
    """
    time_series_data = load_time_series_data()

    new_cases = (
        # Calculate global totals for each day
        time_series_data[["Date", category]]
        .groupby("Date")
        .sum()
        # Calculate daily changes
        .diff()
        # Remove negative values. The values should ideally be positive if new
        # cases occured, and zero if none were observed. But the data
        # occasionally yields negative daily differences.
        .clip(lower=0)
        # Rename the resultant dataframe approrpiately
        .rename(columns={category: f"{category} (New)"})
    )

    colors = {
        "Confirmed": "#4da6ff",
        "Active": "#ef553b",
        "Recovered": "#00cc00",
        "Deaths": "#5c615f",
    }

    new_cases_barplot = px.bar(
        new_cases, color_discrete_sequence=[colors[category]]
    )
    new_cases_barplot.update_layout(
        paper_bgcolor="#f0ffff", plot_bgcolor="#f0ffff"
    )
    new_cases_barplot.update_traces(
        hovertemplate="<b>%{y}</b> <i>%{x}</i><extra></extra>"
    )
    new_cases_barplot.update_xaxes(fixedrange=True)
    new_cases_barplot.update_yaxes(fixedrange=True, title="Number of Cases")

    return new_cases_barplot
