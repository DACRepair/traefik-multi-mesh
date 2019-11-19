import os

DB_URI = str(os.getenv("DB_URI", "mysql+pymysql://root:test@127.0.0.1/tmm"))

PANEL_PORT = int(os.getenv("PANEL_PORT", 5000))
PANEL_HOST = str(os.getenv("PANEL_HOST", "0.0.0.0"))
PANEL_SECRET = str(os.getenv("PANEL_SECRET", "abcdefgchangeme12345"))

TRAEFIK_URL = str(os.getenv("TRAEFIK_URL", "http://10.1.0.48:8080"))
TRAEFIK_USER = str(os.getenv("TRAEFIK_USER", ""))
TRAEFIK_PASS = str(os.getenv("TRAEFIK_PASS", ""))
