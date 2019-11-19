from App.Common.storage import base
from sqlalchemy import Column, String, Integer, Boolean


class Backend(base):
    __tablename__ = "backend"
    backend_id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(255))

    api_url = Column(String(2048))
    end_url = Column(String(2048))

    filter = Column(String(32))


backend_desc = {
    "name": "Name",
    "api_url": "Traefik API URL",
    "end_url": "Traefik Frontend URL",
    "filter": "Endpoint Filter"
}
backend_label = {
    "name": "Backend Name",
    "api_url": "The Traefik API URL (semicolon delimited)",
    "end_url": "The Traefik Frontend Address (where traffic will be routed to, semi-colon delimited)",
    "filter": "Endpoint Filter (looking for this entrypoint to enumerate the rules)"
}
