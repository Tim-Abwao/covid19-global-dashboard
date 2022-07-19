from covid19_dash.dash_app import app
from covid19_dash.data import load_latest_day_data
from dash import dash_table, dcc, html
from dash.dash_table.Format import Format
from dash.dependencies import Input, Output

data = load_latest_day_data().copy()
dates = data.pop("Last Updated Date")

layout = html.Div(
    [
        html.H1("Table of Values"),
        # Introductory text
        dcc.Markdown(
            "The table below displays COVID-19 case information accross "
            f"{data['Location'].nunique()} countries as at "
            f"*{dates[0].strftime('%c')}* UTC. "
            "\n\nThe data used here is obtained from the **Our World in Data**"
            " [owid / covid-19-data][1] GitHub repository."
            "\n\n[1]: https://github.com/owid/covid-19-data"
        ),
        # Data table
        html.Div(
            className="raw-data-table",
            children=[
                dash_table.DataTable(
                    id="table",
                    columns=[
                        {"name": "Location", "id": "Location"},
                        # Apply formatting to numeric columns
                        *[
                            {
                                "name": col,
                                "id": col,
                                "type": "numeric",
                                "format": Format().group(True),
                            }
                            for col in data.columns[3:]
                        ],
                    ],
                    data=data.to_dict("records"),
                    page_size=25,
                    style_cell={
                        "whiteSpace": "normal",
                        "height": "auto",
                    },
                    sort_action="native",
                )
            ],
        ),
        # Data download button
        html.Div(
            style={"margin": "5%"},
            children=[
                html.Button("Download (Excel)", id="download-button"),
                dcc.Download(
                    id="download-dataset", type="application/vnd.ms-excel"
                ),
            ],
        ),
        html.Div(
            className="page-link",
            children=[
                dcc.Link("Compare Countries", href="/compare-countries"),
                dcc.Link("Global Dashboard", href="/"),
            ],
        ),
    ]
)


@app.callback(
    Output("download-dataset", "data"),
    Input("download-button", "n_clicks"),
    prevent_initial_call=True,
)
def download_global_dataset(n_clicks: int) -> dict:
    """Prepare an excel file for download whenever a user clicks on the
    download button.

    Args:
        n_clicks (int): Number of times the download button is clicked.

    Returns:
        dict: Global COVID-19 data in excel format (base64 encoded), and
            meta-data used by the Download component.
    """
    data = load_latest_day_data()
    return dcc.send_data_frame(
        data.to_excel, "covid19-global.xlsx", index=False
    )
