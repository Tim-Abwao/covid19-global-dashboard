import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
from cov19_dash.dash_app import app
from cov19_dash.data import load_time_series_data


time_series_data = load_time_series_data()
latest_day_data = (
    time_series_data.query('Date == @time_series_data["Date"].max()')
    .drop('Date', 1)  # Leave only case data
    .set_index('Country/Region')
)

layout = html.Div([
    html.Div(className='countries-container', children=[
        html.Div(children=[
            dcc.Dropdown(
                id='countries',
                options=[
                    {'label': country, 'value': country}
                    for country in latest_day_data.index
                ],
                multi=True,
                clearable=False,
                persistence=True,
                placeholder='Select a Country',
                value=['Kenya', 'Uganda', 'Tanzania']
            ),
            dcc.RadioItems(
                id='category-countries',
                options=[
                    {'label': 'Confirmed Cases', 'value': 'Confirmed'},
                    {'label': 'Recovered', 'value': 'Recovered'},
                    {'label': 'Deaths', 'value': 'Deaths'}
                ],
                value='Confirmed'
            ),
            dcc.Loading(
                id='lineplot',
                children=dcc.Graph(id='countries-lineplot'),
                color='steelblue'
            )
        ]),
        dcc.Loading(
            id='barplot',
            children=html.Div([dcc.Graph(id='countries-barplot')]),
            color='steelblue'
        )
    ]),
    html.Div(className='pie-chart-container', id='countries-piecharts')
])


@app.callback(
    Output('countries-lineplot', 'figure'),
    [Input('countries', 'value'),
     Input('category-countries', 'value')]
)
def plot_countries_lineplots(countries, category):
    """Get a lineplot of `category` values for various countries."""
    if countries == []:  # If no country is selected
        countries = ['Kenya', 'Uganda', 'Tanzania']
    selection = time_series_data.query('`Country/Region` in @countries')
    lineplot = px.line(selection, x='Date', y=category, color='Country/Region')
    lineplot.update_layout(paper_bgcolor='#f0ffff',
                           plot_bgcolor='#f0ffff')

    return lineplot


@app.callback(
    [Output('countries-barplot', 'figure'),
     Output('countries-piecharts', 'children')],
    Input('countries', 'value')
)
def plot_barplot_and_piecharts(countries):
    """Get a barplot, and pie-charts for each of the supplied countries."""
    if countries == []:  # If no country is selected
        countries = ['Kenya', 'Uganda', 'Tanzania']
    selection = latest_day_data.loc[countries]

    barplot = px.bar(
        selection, y=['Active', 'Deaths', 'Recovered']
    )
    barplot.update_layout(paper_bgcolor='#f0ffff', plot_bgcolor='#f0ffff')

    pie_charts = []
    for country, row in selection.iterrows():
        cases = row.loc[['Active', 'Deaths', 'Recovered']]
        fig = px.pie(
            values=cases, names=cases.index, color=cases.index, title=country,
            hole=0.4
        )
        fig.update_layout(paper_bgcolor='#f0ffff', plot_bgcolor='#f0ffff')
        div = html.Div(
            dcc.Graph(id=f'{country}-pie-chart', figure=fig)
        )
        pie_charts.append(div)

    return barplot, pie_charts
