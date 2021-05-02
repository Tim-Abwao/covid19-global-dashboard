import dash_core_components as dcc
import dash_html_components as html
import dash_table
from cov19_dash.data import load_latest_day_data

data = load_latest_day_data()
dates = data.pop('Date')


layout = html.Div([
    html.H1('Table of Values'),
    dcc.Markdown(f"""
The table below displays the number of *confirmed* cases, *recoveries* and
 *death* cases accross {data['Country/Region'].nunique()} countries as at
 *{dates.max().strftime('%c')}* UTC.

The data used here is obtained from the [JHU CSSE COVID-19 Data][1]
 repository, specifically the global [csse_covid_19_time_series][2] files.

[1]: https://github.com/CSSEGISandData/COVID-19
[2]: https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_\
data/csse_covid_19_time_series
"""),
    dash_table.DataTable(
        id='table',
        columns=[{"name": col, "id": col}for col in data.columns],
        data=data.to_dict('records'),
        sort_action='native',
        page_size=50,
    )
])
