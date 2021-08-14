import dash_core_components as dcc
import dash_html_components as html
import dash_table
from cov19_dash.dash_app import app
from cov19_dash.data import load_latest_day_data
from dash.dependencies import Input, Output
from dash_table.Format import Format

data = load_latest_day_data()
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
            " [owid / covid-19-data][1] GitHub repository. You can "
            "[view the original here][2]."
            "\n\n[1]: https://github.com/owid/covid-19-data"
            "\n[2]: https://github.com/owid/covid-19-data/blob/master/public/"
            "data/latest/owid-covid-latest.csv"
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
                    page_size=50,
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
    ]
)


@app.callback(
    Output("download-dataset", "data"),
    Input("download-button", "n_clicks"),
    prevent_initial_call=True,
)
def download_global_dataset(n_clicks) -> dict:
    """Prepare a csv file for download whenever a user clicks on the download
    button.

    Parameters
    ----------
    n_clicks : int
        The number of times the download button is clicked

    Returns
    -------
    dict
        Global covid-19 data in csv format (base64 encoded), and meta data
        used by the Download component.
    """
    data = load_latest_day_data()
    return dcc.send_data_frame(data.to_excel, "covid19-global.xlsx")
