import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from cov19_dash.dash_app import app
from cov19_dash.tabs import countries, tables, worldwide

server = app.server

app.layout = html.Div(
    [
        dcc.Tabs(
            id="tabs",
            value="tab-1",
            children=[
                dcc.Tab(label="Global Map", value="tab-1"),
                dcc.Tab(label="Compare Countries", value="tab-2"),
                dcc.Tab(label="Raw Data", value="tab-3"),
            ],
            colors={
                "border": "teal",
                "primary": "#1975FA",
                "background": "#f0ffff",
            },
        ),
        html.Div(id="tabs-content", className="tab-content"),
    ]
)


@app.callback(Output("tabs-content", "children"), Input("tabs", "value"))
def render_content(tab):
    """Display the content for the selected tab."""
    if tab == "tab-1":
        return worldwide.layout
    elif tab == "tab-2":
        return countries.layout
    elif tab == "tab-3":
        return tables.layout


if __name__ == "__main__":
    app.run_server(debug=True)
