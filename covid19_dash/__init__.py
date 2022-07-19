import logging

import waitress

from covid19_dash.dashboard import server

# Set waitress.queue logging level to ERROR
logging.getLogger("waitress.queue").setLevel(logging.ERROR)


def run_server() -> None:
    """Start the dashboard server."""
    waitress.serve(server, host="localhost", port=8000)
