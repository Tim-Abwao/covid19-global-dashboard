import dash

app = dash.Dash(
    "cov19_dash",
    suppress_callback_exceptions=True,
    title="COVID-19 Dashboard",
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0",
        }
    ],
)

server = app.server
