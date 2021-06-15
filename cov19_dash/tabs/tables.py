import dash_core_components as dcc
import dash_html_components as html
import dash_table
from cov19_dash.dash_app import app
from cov19_dash.data import (
    check_if_data_is_stale,
    load_latest_day_data,
    load_time_series_data,
)
from dash.dependencies import Input, Output
from dash_table.Format import Format

# Refresh datasets
check_if_data_is_stale()

data = load_latest_day_data()
dates = data.pop("Date")


layout = html.Div(
    [
        html.H1("Table of Values"),
        # Introductory text
        dcc.Markdown(
            f"""
The table below displays the number of *confirmed* cases, *recoveries* and
 *death* cases accross {data['Country/Region'].nunique()} countries as at
 *{dates.max().strftime('%c')}* UTC.

The data used here is obtained from the [JHU CSSE COVID-19 Data][1]
 repository, specifically the global [csse_covid_19_time_series][2] files.

[1]: https://github.com/CSSEGISandData/COVID-19
[2]: https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_\
data/csse_covid_19_time_series
"""
        ),
        # Data table
        html.Div(
            className="raw-data-table",
            children=[
                dash_table.DataTable(
                    id="table",
                    columns=[
                        {"name": "Country/Region", "id": "Country/Region"},
                        {
                            "name": "Confirmed",
                            "id": "Confirmed",
                            "type": "numeric",
                            "format": Format().group(True),
                        },
                        {
                            "name": "Recovered",
                            "id": "Recovered",
                            "type": "numeric",
                            "format": Format().group(True),
                        },
                        {
                            "name": "Active",
                            "id": "Active",
                            "type": "numeric",
                            "format": Format().group(True),
                        },
                        {
                            "name": "Deaths",
                            "id": "Deaths",
                            "type": "numeric",
                            "format": Format().group(True),
                        },
                        {"name": "Lat", "id": "Lat", "type": "numeric"},
                        {"name": "Long", "id": "Long", "type": "numeric"},
                    ],
                    data=data.to_dict("records"),
                    sort_action="native",
                    page_size=50,
                )
            ],
        ),
        # Data download button
        html.Div(
            style={"margin": "5%"},
            children=[
                html.Button("Download CSV", id="download-button"),
                dcc.Download(id="download-dataset", type="text/csv"),
            ],
        ),
    ]
)


@app.callback(
    Output("download-dataset", "data"),
    Input("download-button", "n_clicks"),
    prevent_initial_call=True,
)
def download_global_dataset(n_clicks):
    """Prepare a csv file for download whenever a user clicks on the download
    button.

    Parameters
    ----------
    n_clicks : int
        The number of times the download button is clicked

    Returns
    -------
    Global covid-19 time series data in csv format.
    """
    data = load_time_series_data()
    return dcc.send_data_frame(data.to_csv, "covid19-global.csv")
