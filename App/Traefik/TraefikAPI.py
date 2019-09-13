import json
from requests import Session


class Traefik:
    def __init__(self, base_url: str, user: str = '', password: str = ''):
        self.base_url = base_url.rstrip("/") + "/api"
        self.session = Session()

        if len(user) > 0:
            self._auth = (user, password,)
        else:
            self._auth = None

    def _get(self, method: str, params: dict = None):
        return self.session.get(url="{}/{}".format(self.base_url, method), params=params, auth=self._auth)

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
        return self.session.put(url="{}/{}".format(self.base_url, method), data=payload, auth=self._auth)
