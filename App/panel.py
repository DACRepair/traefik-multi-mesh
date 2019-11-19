from App.Common.web import app
from App.Common.config import PANEL_PORT, PANEL_HOST


def run_web():
    return app.run(PANEL_HOST, PANEL_PORT)
