from App.Common.config import TRAEFIK_URL, TRAEFIK_USER, TRAEFIK_PASS
from App.Common.storage import session_builder
from App.Model.Backend import Backend
from App.Traefik.rest import Traefik


class Instance:
    def __init__(self, instance: dict):
        self.id = instance['backend_id']
        self.name = instance['name']
        self.filter = instance['filter'] if instance['filter'] is not None else ''
        self.enabled = instance['enabled']
        self.weight = instance['weight']

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
        self.traefik = Traefik(TRAEFIK_URL, TRAEFIK_USER, TRAEFIK_PASS)

    def update_instances(self):
        session = session_builder()
        instances = session.query(Backend).filter(Backend.enabled)
        instances = instances.order_by(Backend.weight.desc(), Backend.name.desc()).all()
        instances = [{c.name: getattr(i, c.name) for c in i.__table__.columns} for i in instances]
        self.instances = [Instance(x) for x in instances]

    def get_backends(self):
        backends = {}
        for instance in self.instances:
            backends[instance.name] = {
                "loadBalancer": {"method": "drr"},
                "servers": {}
            }
            i = 0
            for server in instance.endpoints:
                server = {"server{}".format(i): {"weight": 0, "url": server}}
                backends[instance.name]["servers"].update(server)
                i += 1

        return backends

    def get_frontends(self):
        frontends = {}
        rules = []
        for instance in self.instances:
            traefik = Traefik(";".join(instance.api_endpoints))
            for provider in traefik.provider().values():
                if len(provider) > 0:
                    provider = provider['frontends']
                    for name, rule in provider.items():
                        if True in [x in instance.filter for x in rule['entryPoints']] or len(instance.filter) == 0:
                            r = str(list(rule['routes'].values())[0]['rule'])
                            if r not in rules:
                                rules.append(r)
                                rule['backend'] = instance.name
                                frontends["{}-{}".format(str(instance.name), str(name).split("_")[-1])] = rule
        return frontends

    def do_sync(self):
        self.update_instances()
        if "error" not in self.traefik.health().keys():
            payload = {"backends": self.get_backends(), "frontends": self.get_frontends()}
            return self.traefik.put("rest", payload).status_code == 200
