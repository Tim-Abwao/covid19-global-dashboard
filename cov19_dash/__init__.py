import logging

import waitress

from cov19_dash.dashboard import server

logger = logging.getLogger('waitress')
logger.setLevel(logging.ERROR)


def run_server():
    """Start the dashboard server."""
    waitress.serve(server, host='localhost', port=8000)
