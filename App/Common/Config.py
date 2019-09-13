import os
from configparser import ConfigParser
from glob import glob


class Instance(object):
    class _API:
        def __init__(self, data):
            self.url = data['url']
            self.user = data['user']
            self.password = data['password']
            self.entrypoint = data['entrypoint']

        def __str__(self):
            return str(self.__dict__)

        def __repr__(self):
            return self.__str__()

    class _Endpoint:
        def __init__(self, name: str = "", address: str = ""):
            self.name = name
            self.address = address

        def __str__(self):
            return str(self.__dict__)

        def __repr__(self):
            return self.__str__()

    name: str
    api: _API
    endpoints: [_Endpoint()]

    def __init__(self, name: str, data: dict):
        self.name = name
        self.api = self._API(data['api'])
        self.endpoints = [self._Endpoint(n, a) for n, a in data['endpoints'].items()]

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()


class Config:
    def __init__(self, conf_dir):
        self.conf_dir = os.path.normpath(conf_dir)
        confs = list(glob(conf_dir + "/*.ini"))
        self.instances = []
        for conf in confs:
            name = str(os.path.basename(conf).split(".")[0])
            if name.startswith("_"):
                pass
            else:
                cp = ConfigParser()
                cp.read(conf)
                data = {s: {k: self._clean_para(v) for k, v in dict(cp.items(s)).items()} for s in cp.sections()}
                self.instances.append(name)
                setattr(self, name, Instance(name, data))

    def get(self, endpoint):
        endpoint: Instance = getattr(self, endpoint)
        return endpoint

    def _clean_para(self, s: str):
        return s.lstrip('"').rstrip('"')
