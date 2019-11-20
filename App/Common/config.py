import os


def getenv(env, default=None):
    return str(os.getenv(env, default)).lstrip('"').rstrip('"').lstrip("'").rstrip("'")


DB_URI = str(getenv("DB_URI", "mysql+pymysql://root:test@127.0.0.1/tmm"))

REFRESH_RATE = int(getenv("REFRESH_RATE", "60"))

PANEL_PORT = int(getenv("PANEL_PORT", 5000))
PANEL_HOST = str(getenv("PANEL_HOST", "0.0.0.0"))
PANEL_SECRET = str(getenv("PANEL_SECRET", "abcdefgchangeme12345"))

TRAEFIK_URL = str(getenv("TRAEFIK_URL", "http://10.1.0.48:8080"))
TRAEFIK_USER = str(getenv("TRAEFIK_USER", ""))
TRAEFIK_PASS = str(getenv("TRAEFIK_PASS", ""))
