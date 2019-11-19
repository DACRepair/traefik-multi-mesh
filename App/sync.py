import dictdiffer

from App.Common.config import TRAEFIK_URL, TRAEFIK_USER, TRAEFIK_PASS
from App.Common.storage import session_builder
from App.Model.Backend import Backend
from App.Traefik.rest import Traefik
import pprint


class Instance:
    def __init__(self, instance: dict):
        self.id = instance['backend_id']
        self.name = instance['name']
        self.filter = instance['filter']
        self.enabled = instance['enabled']

        self.api_endpoints = []
        for api in str(instance['api_url']).split(";"):
            self.api_endpoints.append(api)

        self.endpoints = []
        for endpoint in str(instance["end_url"]).split(";"):
            self.endpoints.append(endpoint)

    def __str__(self):
        return "<Instance: {}>".format(self.name)

    def __repr__(self):
        return self.__str__()


class SyncServer:
    instances = []

    def __init__(self):
        self.update_instances()
        self.traefik = Traefik(TRAEFIK_URL, TRAEFIK_USER, TRAEFIK_PASS)

    def _get_instances(self):
        session = session_builder()
        return [{c.name: getattr(i, c.name) for c in i.__table__.columns} for i in session.query(Backend).all()]

    def update_instances(self):
        self.instances = [Instance(x) for x in self._get_instances()]

    def _get_instance_providers(self, instance: Instance):
        return Traefik(";".join(instance.api_endpoints))

    def get_frontends(self):
        frontends = {}
        for instance in self.instances:
            frontends[instance.id] = {}
            i = list(self._get_instance_providers(instance).provider().values())
            for i in [x['frontends'] for x in i if len(x) > 0]:
                frontends[instance.id].update(i)

        return frontends


s = SyncServer()
pprint.pprint(s.get_frontends())
