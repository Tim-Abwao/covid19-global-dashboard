import logging

import waitress

from covid19_dash.dash_app import app

# Set waitress.queue logging level to ERROR
logging.getLogger("waitress.queue").setLevel(logging.ERROR)


def run_server() -> None:
    """Start the dashboard server."""
    waitress.serve(app.server, host="localhost", port=8000)
