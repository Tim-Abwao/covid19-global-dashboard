import dash


app = dash.Dash('cov19_dash', suppress_callback_exceptions=True,
                title='Covid19 Dashboard')
server = app.server
