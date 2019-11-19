import os

DB_URI = str(os.getenv("DB_URI", "sqlite:///./data/database.sqlite"))

PANEL_PORT = int(os.getenv("PANEL_PORT", 5000))
PANEL_HOST = str(os.getenv("PANEL_HOST", "0.0.0.0"))
PANEL_SECRET = str(os.getenv("PANEL_SECRET", "abcdefgchangeme12345"))

TRAEFIK_URL = str(os.getenv("TRAEFIK_URL", "http://127.0.0.1:8080"))
