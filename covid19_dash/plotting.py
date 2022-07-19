import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame, Series


def plot_value(
    value: int | float, title: str, color: str = "teal"
) -> go.Figure:
    """Get a numeric metric as a card.

    Args:
        value (int | float): Amount.
        title (str): Metric name.
        color (str, optional): Font color. Defaults to "teal".

    Returns:
        plotly.graph_objs._figure.Figure: Indicator chart.
    """
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=value,
            title={"text": title},
            number={"valueformat": ",.0f", "font": {"color": color}},
        )
    )
    fig.update_layout(
        font_color="#333",
        font_family="serif",
        paper_bgcolor="#f0ffff",
        width=220,
        margin={"l": 20, "r": 20, "t": 50, "b": 20},
        height=150,
    )
    return fig


def plot_spark_line(data: Series, color: str, title: str) -> go.Figure:
    """Get a spark-line.

    Args:
        data (pandas.Series): Values to plot.
        color (str): Line color.
        title (str): Plot title.

    Returns:
        plotly.graph_objs._figure.Figure: Spark-line.
    """
    fig = go.Figure(
        go.Scatter(
            x=data.index,
            y=data,
            line={"width": 2, "color": color},
            showlegend=False,
            hovertemplate="<i>%{x}:</i> <b>%{y:,}</b><extra></extra>",
        ),
    )
    fig.add_trace(
        go.Scatter(
            x=[data.index[-1]],
            y=[data.iloc[-1]],
            cliponaxis=False,
            hovertemplate="<i>%{x}:</i> <b>%{y:,.0f}</b><extra></extra>",
            marker={"size": 5, "color": color, "symbol": "diamond"},
            mode="markers+text",
            text=f"{data.iloc[-1]:,.0f}",
            textfont={"size": 9},
            textposition="middle right",
            showlegend=False,
        )
    )
    fig.update_xaxes(fixedrange=True, tickfont={"size": 9})
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        font_color="#333",
        font_family="serif",
        height=140,
        margin={"l": 0, "r": 35, "t": 50, "b": 0},
        paper_bgcolor="#f0ffff",
        plot_bgcolor="#f0ffff",
        title=title,
        title_x=0.5,
        width=240,
    )
    return fig


def plot_gauge_chart(
    value: int | float,
    reference: int | float,
    title: str,
    color: str = "steelblue",
) -> go.Figure:
    """Get a gauge-plot.

    Args:
        value (int | float): Current value.
        reference (int | float): Target value.
        title (str): Chart title.
        color (str, optional): Gauge color. Defaults to "steelblue".

    Returns:
        plotly.graph_objs._figure.Figure: Gauge plot.
    """
    fig = go.Figure(
        go.Indicator(
            mode="gauge+delta+number",
            value=value,
            delta={"reference": reference},
            gauge={
                "axis": {"range": [None, reference]},
                "bar": {"color": color},
                "bgcolor": "#f0ffff",
            },
            title={"text": title, "font": {"size": 17}},
        )
    )
    fig.update_layout(
        font_color="#333",
        font_family="serif",
        height=250,
        margin={"l": 20, "r": 0, "t": 20, "b": 0},
        paper_bgcolor="#f0ffff",
        title_x=0.5,
        width=250,
    )
    return fig


def plot_global_map(data: DataFrame, category: str, date: str) -> go.Figure:
    """Get a global choropleth map.

    Args:
        data (pandas.DataFrame): Values to plot.
        category (str): Colouring dimension.
        date (str): Date of last update.

    Returns:
        plotly.graph_objs._figure.Figure: Choropleth map.
    """
    if category in {
        "Total Cases",
        "Total Cases Per Million",
        "New Cases",
        "Total Deaths",
    }:
        colors = ["silver", "gold", "#f51"]
    elif category in {
        "People Fully Vaccinated",
        "People Fully Vaccinated Per Hundred",
        "Hospital Beds Per Thousand",
        "Total Vaccinations",
        "Life Expectancy",
    }:
        colors = ["silver", "#fe7", "lime"]
    elif category in {"Aged 70 Older", "Diabetes Prevalence"}:
        colors = ["silver", "#227"]
    fig = px.choropleth(
        data,
        locations="Location",
        locationmode="country names",
        color=category,
        color_continuous_scale=colors,
        title=f"<i>{category}</i> as at {date}",
    )
    fig.update_geos(
        bgcolor="#f0ffff",
        fitbounds="locations",
        showframe=False,
        resolution=110,
    )
    fig.update_layout(
        font_color="#333",
        font_family="serif",
        paper_bgcolor="#f0ffff",
        margin={"l": 0, "r": 0, "t": 50, "b": 0},
        dragmode=False,
    )
    fig.update_traces(
        hovertemplate=(f"<b>%{{location}}</b><br>{category}: <b>%{{z:,}}</b>")
    )
    fig.update_coloraxes(
        colorbar=dict(
            len=0.6,
            thickness=0.032,
            thicknessmode="fraction",
            tickfont_size=9,
            title_text="",
        )
    )
    return fig


def plot_pie_chart(data: DataFrame, metric: str, countries: list) -> go.Figure:
    """Get a donut-chart (pie-chart).

    Args:
        data (pandas.DataFrame): Values to plot.
        metric (str): Column to plot.
        countries (list): Selected countries.

    Returns:
        plotly.graph_objs._figure.Figure: Donut-chart.
    """
    fig = px.pie(
        values=data[metric],
        names=countries,
        color=countries,
        hole=0.5,
        title=metric,
    )
    fig.update_layout(
        font_color="#333",
        font_family="serif",
        paper_bgcolor="#f0ffff",
        plot_bgcolor="#f0ffff",
        margin={"l": 0, "r": 0, "t": 50, "b": 0},
    )
    fig.update_traces(
        hovertemplate="<b>%{label}:</b> %{value:,}<extra></extra>"
    )
    return fig


def plot_lines(data: DataFrame, category: str) -> go.Figure:
    """Get a comparative line-plot.

    Args:
        data (pandas.DataFrame): Values to plot.
        category (str): Column to plot.

    Returns:
        plotly.graph_objs._figure.Figure: Line-plot.
    """
    fig = px.line(data, x="Date", y=category, color="Country/Region")
    fig.update_layout(
        font_color="#333",
        font_family="serif",
        hovermode="x unified",
        paper_bgcolor="#f0ffff",
        plot_bgcolor="#f0ffff",
        margin={"l": 0, "r": 0, "t": 50, "b": 0},
    )
    fig.update_traces(hovertemplate="<i>%{x}</i><br><b>%{y:,}</b>")
    fig.update_xaxes(
        fixedrange=True,
    )
    fig.update_yaxes(fixedrange=True)
    return fig
