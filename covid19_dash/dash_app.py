import dash

app = dash.Dash(
    "covid19_dash",
    title="COVID-19 Dashboard",
    external_scripts=[
        "https://cdn.plot.ly/plotly-2.13.1.min.js",
    ],
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0",
        }
    ],
    use_pages=True
)
