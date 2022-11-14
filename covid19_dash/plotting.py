import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame, Series


def plot_value(
    current_value: int | float,
    delta: int | float,
    title: str,
    color: str = "teal",
) -> go.Figure:
    """Get a numeric metric as a card.

    Args:
        current_value (int | float): Amount.
        delta (int | float): Magnitude of change from previous amount.
        title (str): Metric name.
        color (str, optional): Font color. Defaults to "teal".

    Returns:
        plotly.graph_objs._figure.Figure: Indicator chart.
    """
    fig = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=current_value,
            delta=dict(
                reference=current_value - delta,
                valueformat=",.0f",
            ),
            title={"text": title, "font_size": 17},
            number={"valueformat": ",.0f", "font": {"color": color}},
        )
    )
    fig.update_layout(
        font_color=color,
        font_family="serif",
        height=150,
        margin={"l": 20, "r": 20, "t": 50, "b": 20},
        paper_bgcolor="#236",
        width=240,
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
            textfont={"size": 10},
            textposition="middle right",
            showlegend=False,
        )
    )
    fig.update_xaxes(fixedrange=True, tickfont={"size": 9}, showgrid=False)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        font_color=color,
        font_family="serif",
        height=140,
        margin={"l": 0, "r": 35, "t": 50, "b": 0},
        paper_bgcolor="#236",
        plot_bgcolor="#236",
        title=title,
        title_x=0.5,
        width=240,
    )
    return fig


def plot_gauge_chart(
    value: int | float,
    reference: int | float,
    title: str,
    color: str,
) -> go.Figure:
    """Get a gauge-plot.

    Args:
        value (int | float): Current value.
        reference (int | float): Target value.
        title (str): Chart title.
        color (str, optional): Gauge color.

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
                "bgcolor": "#236",
            },
            title={"text": title, "font": {"size": 17}},
        )
    )
    fig.update_layout(
        font_color=color,
        font_family="serif",
        height=250,
        margin={"l": 20, "r": 0, "t": 20, "b": 0},
        paper_bgcolor="#236",
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
        "Aged 70 Older",
        "Diabetes Prevalence",
    }:
        colors = ["#236", "#fe7", "#f77"]
    elif category in {
        "People Fully Vaccinated",
        "People Fully Vaccinated Per Hundred",
        "Hospital Beds Per Thousand",
        "Total Vaccinations",
        "Life Expectancy",
    }:
        colors = ["#236", "#fe7", "#2b2"]

    fig = px.choropleth(
        data,
        locations="Location",
        locationmode="country names",
        color=category,
        color_continuous_scale=colors,
        title=f"<i>{category}</i> as at {date}",
    )
    fig.update_layout(
        font_color="#ddd",
        font_family="serif",
        paper_bgcolor="#236",
        margin={"l": 0, "r": 0, "t": 50, "b": 0},
        dragmode=False,
    )
    fig.update_traces(
        hovertemplate=(f"<b>%{{location}}</b><br>{category}: <b>%{{z:,}}</b>"),
        marker_line_color="#777",
        marker_line_width=0.5,
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
    fig.update_geos(
        bgcolor="#236",
        fitbounds="locations",
        showframe=False,
        resolution=110,
    )
    return fig


def plot_column_chart(data: DataFrame, metric: str) -> go.Figure:
    """Get a column chart.

    Args:
        data (pandas.DataFrame): Values to plot.
        metric (str): Info to plot.

    Returns:
        plotly.graph_objs._figure.Figure: Column chart.
    """
    fig = px.bar(
        data,
        x="Location",
        y=metric,
        color="Location",
        height=320,
        text="Location",
        title=metric,
    )
    fig.update_layout(
        font_color="#ddd",
        font_family="serif",
        paper_bgcolor="#236",
        plot_bgcolor="#236",
        margin={"l": 0, "r": 0, "t": 50, "b": 0},
        uniformtext_minsize=8,
    )
    fig.update_traces(
        cliponaxis=False,
        showlegend=False,
        hovertemplate="<b>%{label}:</b> %{value:,.2f}<extra></extra>",
        textfont_size=11,
    )
    fig.update_xaxes(
        categoryorder="total descending", fixedrange=True, visible=False
    )
    fig.update_yaxes(fixedrange=True, gridcolor="#444")
    return fig


def plot_lines(data: DataFrame, category: str) -> go.Figure:
    """Get a comparative line-plot.

    Args:
        data (pandas.DataFrame): Values to plot.
        category (str): Info to plot.

    Returns:
        plotly.graph_objs._figure.Figure: Line-plot.
    """
    fig = px.line(data, x="Date", y=category, color="Country/Region")
    fig.update_layout(
        font_color="#ddd",
        font_family="serif",
        hovermode="x unified",
        legend_font_size=11,
        paper_bgcolor="#236",
        plot_bgcolor="#236",
        margin={"l": 0, "r": 0, "t": 50, "b": 0},
    )
    fig.update_traces(hovertemplate="<i>%{x}</i><br><b>%{y:,}</b>")
    fig.update_xaxes(fixedrange=True, showgrid=False)
    fig.update_yaxes(fixedrange=True, gridcolor="#444")
    return fig
