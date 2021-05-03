import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from cov19_dash.dash_app import app
from dash.dependencies import Input, Output
from cov19_dash.data import load_latest_day_data, check_if_data_is_stale


layout = html.Div(className='global-container', children=[
    html.Div(id='global-sidebar', children=[
        # Display global totals
        html.Div(id='totals', className='totals-container')
    ]),
    html.Div(id='global-map-container', children=[
        # Select case category
        dcc.RadioItems(
            id='category',
            options=[
                {'label': 'Confirmed', 'value': 'Confirmed'},
                {'label': 'Active', 'value': 'Active'},
                {'label': 'Recovered', 'value': 'Recovered'},
                {'label': 'Deaths', 'value': 'Deaths'}
            ],
            value='Confirmed'),
        # Display a geo-scatterplot
        dcc.Loading(
            id='refresh-data',
            children=dcc.Graph(id='global-bubble-map'),
            color='steelblue'
        )
    ], className='global-map-container')
])


@app.callback(
    [Output('totals', 'children'),
     Output('global-bubble-map', 'figure')],
    Input('category', 'value')
)
def plot_global_bubble_map(category):
    check_if_data_is_stale()
    data = load_latest_day_data()
    data_date = data["Date"].max().strftime('%A, %b %-d %Y')
    # Prepare totals content
    totals = data[
        ['Confirmed', 'Recovered', 'Active', 'Deaths']
    ].sum().items()
    totals_content = html.Div(children=sum([
        (html.H2(col), html.H1(f'{value:,}', id=f'{col.lower()}-total'))
        for col, value in totals
    ], start=())
    )
    # Negative values in the size parameter raise a ValueError
    data[category] = data[category].clip(lower=0)

    geo_scatterplot = px.scatter_geo(
        data, lat='Lat', lon='Long', color=category, size=category,
        size_max=60, hover_name='Country/Region',
        color_continuous_scale=['#00334d', '#ffff77'],
        custom_data=[category],
        title=f'Global Totals <i>({category})</i> as at {data_date}'
    )
    geo_scatterplot.update_geos(
        bgcolor='#f0ffff', showcountries=True, countrycolor='#72a0c1',
        showframe=False, coastlinecolor='skyblue'
    )
    geo_scatterplot.update_layout(paper_bgcolor='#f0ffff')
    geo_scatterplot.update_traces(
        hovertemplate=f'''<b>%{{hovertext}}</b><br>
{category}: %{{customdata[0]:,}}'''
    )
    return totals_content, geo_scatterplot
