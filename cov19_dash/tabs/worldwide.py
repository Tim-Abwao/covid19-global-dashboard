import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from cov19_dash.dash_app import app
from dash.dependencies import Input, Output
from cov19_dash.data import load_latest_day_data


layout = html.Div([
    html.H1('Global'),
    dcc.RadioItems(
        id='category',
        options=[
            {'label': 'Confirmed Cases', 'value': 'Confirmed'},
            {'label': 'Recovered', 'value': 'Recovered'},
            {'label': 'Deaths', 'value': 'Deaths'}
        ],
        value='Confirmed'
    ),
    dcc.Graph(id='global-bubble-map')
])


@app.callback(
    Output('global-bubble-map', 'figure'),
    Input('category', 'value')
)
def plot_global_bubble_map(category):
    data = load_latest_day_data()
    fig = px.scatter_geo(
        data, lat='Lat', lon='Long', color=category, size=category,
        size_max=60, height=600,
    )
    fig.update_geos(
        bgcolor='white', showcountries=True, countrycolor='skyblue',
        showframe=False, coastlinecolor='skyblue'
    )

    return fig
