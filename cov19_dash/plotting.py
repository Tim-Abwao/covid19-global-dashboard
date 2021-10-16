from pandas.core.frame import DataFrame
from pandas.core.series import Series
import plotly.express as px
import plotly.graph_objects as go
from typing import Union


def plot_value(
    value: Union[int, float], title: str, color: str = "teal"
) -> go.Figure:
    """Get a numeric metric as a card.

    Parameters
    ----------
    value : Union[int, float]
        The number to display
    title : str
        Card title
    color : str, optional
        Font color for displayed text, by default teal

    Returns
    -------
    plotly.graph_objs._figure.Figure
        An indicator chart.
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
        paper_bgcolor="#f0ffff",
        width=220,
        margin={"l": 20, "r": 20, "t": 50, "b": 20},
        height=150,
    )
    return fig


def plot_spark_line(data: Series, color: str, title: str) -> go.Figure:
    """Get a spark-like lineplot.

    Parameters
    ----------
    data : Series
        The data to plot
    color : str
        Line color
    title : str
        Graph title

    Returns
    -------
    plotly.graph_objs._figure.Figure
        A lineplot of the data.
    """
    fig = go.Figure(
        go.Scatter(
            x=data.index,
            y=data,
            line={"width": 3, "color": color},
            showlegend=False,
            hovertemplate="<i>%{x}:</i> <b>%{y:,}</b><extra></extra>",
        ),
    )
    fig.add_trace(
        go.Scatter(
            x=[data.index[-1]],
            y=[data.iloc[-1]],
            mode="markers+text",
            marker={"size": 8, "color": color},
            text=f"{data.iloc[-1]:,.0f}",
            textposition="top center",
            textfont={"size": 8},
            showlegend=False,
        )
    )
    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        width=220,
        height=140,
        margin={"l": 0, "r": 0, "t": 50, "b": 0},
        title=title,
        plot_bgcolor="#f0ffff",
        paper_bgcolor="#f0ffff",
    )
    return fig


def plot_gauge_chart(
    value: Union[int, float],
    reference: Union[int, float],
    title: str,
    color: str = "teal",
) -> go.Figure:
    """Get a gauge-plot for a given value.

    Parameters
    ----------
    value : Union[int, float]
        The current value
    reference : Union[int, float]
        The target value
    title : str
        Chart title
    color : str, optional
        Gauge color, by default "teal"

    Returns
    -------
    plotly.graph_objs._figure.Figure
        A gauge-plot of the supplied data.
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
            title={"text": title, "align": "left", "font": {"size": 18}},
        )
    )
    fig.update_layout(
        paper_bgcolor="#f0ffff",
        width=250,
        margin={"l": 20, "r": 0, "t": 20, "b": 0},
        height=250,
    )
    return fig


def plot_global_map(data: DataFrame, category: str, date: str) -> go.Figure:
    """Get a choropleth map of the natural world (global).

    Parameters
    ----------
    data : DataFrame
        The data to plot
    category : str
        The column to when colouring
    date : str
        The data's last-updated date

    Returns
    -------
    plotly.graph_objs._figure.Figure
        A choropleth map.
    """
    fig = px.choropleth(
        data,
        locations="Location",
        locationmode="country names",
        color=category,
        color_continuous_scale=["#00334d", "#ffff77"],
        title=f"<i>{category}</i> as at {date}",
    )
    fig.update_geos(
        bgcolor="#f0ffff",
        fitbounds="locations",
        showframe=False,
        resolution=110,
    )
    fig.update_layout(
        paper_bgcolor="#f0ffff",
        margin={"l": 0, "r": 0, "t": 50, "b": 0},
        dragmode=False,
    )
    fig.update_traces(
        hovertemplate=(f"<b>%{{location}}</b><br>{category}: <b>%{{z:,}}</b>")
    )
    fig.update_coloraxes(showscale=False)
    return fig


def plot_pie_chart(data: DataFrame, metric: str, countries: list) -> go.Figure:
    """Get a donut-chart (pie-chart) of the given data.

    Parameters
    ----------
    data : DataFrame
        The data to plot
    metric : str
        The column to plot
    countries : list
        A list of countries

    Returns
    -------
    plotly.graph_objs._figure.Figure
        A pie chart.
    """
    fig = px.pie(
        values=data[metric],
        names=countries,
        color=countries,
        title=metric,
        hole=0.5,
    )
    fig.update_layout(
        paper_bgcolor="#f0ffff",
        plot_bgcolor="#f0ffff",
        margin={"l": 0, "r": 0, "t": 50, "b": 0},
    )
    fig.update_traces(
        hovertemplate="<b>%{label}:</b> %{value:,}<extra></extra>"
    )
    return fig


def plot_lines(data: DataFrame, category: str) -> go.Figure:
    """Get a combined line-plot of the given data

    Parameters
    ----------
    data : DataFrame
        The data to plot
    category : str
        The column to plot

    Returns
    -------
    gplotly.graph_objs._figure.Figure
        A line-plot.
    """
    fig = px.line(data, x="Date", y=category, color="Country/Region")
    fig.update_layout(
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
