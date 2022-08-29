import logging

from covid19_dash.dash_app import app

# Set waitress.queue logging level to ERROR
logging.getLogger("waitress.queue").setLevel(logging.ERROR)

server = app.server
