import json
from requests import Session


class Traefik:
    def __init__(self, base_url: str, user: str = '', password: str = ''):
        self.base_urls = base_url.split(";")
        self.base_url = ""
        self.session = Session()

        if len(user) > 0:
            self.session.auth = (user, password,)
        else:
            self.session.auth = None

    def _get(self, method: str, params: dict = None):
        retr = None
        for base_url in self.base_urls:
            base_url = base_url.lstrip("/") + "/api"
            try:
                retr = self.session.get(url="{}/{}".format(base_url, method), params=params)
                break
            except:
                pass
        return retr

    def _put(self, method: str, data):
        retr = None
        for base_url in self.base_urls:
            base_url = base_url.lstrip("/") + "/api"
            try:
                retr = self.session.put(url="{}/{}".format(base_url, method), data=data)
                break
            except:
                pass
        return retr

    def provider(self, provider: str = None) -> [dict, None]:
        method = "providers"
        if provider is not None:
            method = method + "/" + provider
        retr = self._get(method)
        if retr.status_code == 200:
            return retr.json()
        else:
            return None

    def put(self, provider: str = "rest", payload: dict = None):
        method = "providers/{}".format(provider)
        payload = json.dumps(payload)
        return self._put(method, data=payload)
