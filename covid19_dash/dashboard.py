from dash import dcc, html
from dash.dependencies import Input, Output

from covid19_dash.dash_app import app
from covid19_dash.pages import countries, tables, worldwide

server = app.server

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.H1("COVID-19 Global Dashboard"),
        html.Div(id="page-content"),
    ]
)


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_content(pathname: str) -> html.Div:
    """Render the page at the specified `pathname`.

    Args:
        pathname (str): URL endpoint.

    Returns:
        dash.html.Div.Div: Web page content.
    """
    if pathname == "/compare-countries":
        return countries.layout
    elif pathname == "/data":
        return tables.layout
    else:
        return worldwide.layout
