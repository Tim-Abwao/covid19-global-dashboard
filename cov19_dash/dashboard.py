import dash_html_components as html
import dash_core_components as dcc


from dash.dependencies import Input, Output

from dash_app import app
from tabs import worldwide, countries, tables


app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Global', value='tab-1'),
        dcc.Tab(label='Countries', value='tab-2'),
        dcc.Tab(label='Data', value='tab-3'),
    ]),
    html.Div(id='tabs-content')
])


tab_1 = dcc.Input()


@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return worldwide.layout

    elif tab == 'tab-2':
        return countries.layout
    elif tab == 'tab-3':
        return tables.layout


if __name__ == '__main__':
    app.run_server(debug=True)
