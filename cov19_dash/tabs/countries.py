import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
from cov19_dash.dash_app import app
from cov19_dash.data import load_time_series_data


data = load_time_series_data()


layout = html.Div([
    html.H1('Countries'),
    dcc.Dropdown(
        id='countries',
        options=[
            {'label': country, 'value': country}
            for country in data['Country/Region'].unique()
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
    dcc.Graph(id='country-comparison')
])


@app.callback(
    Output('country-comparison', 'figure'),
    [Input('countries', 'value'),
     Input('category-countries', 'value')]
)
def plot_countries_comparison(countries, category):
    if countries == []:  # If no country is selected
        countries = ['Kenya', 'Uganda', 'Tanzania']
    selection = data.query('`Country/Region` in @countries')
    fig = px.line(selection, x='Date', y=category, color='Country/Region')

    return fig
