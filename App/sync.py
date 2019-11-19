from App.Common.storage import session_builder
from App.Model.Backend import Backend


class SyncServer:
    def __init__(self):
        self.instances = [dict(x) for x in self.get_instances()]

    def get_instances(self):
        session = session_builder()
        return session.query(Backend).all()

SyncServer()