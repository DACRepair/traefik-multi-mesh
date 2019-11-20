import json
from requests import Session, Response


class Traefik:
    def __init__(self, base_url: str, user: str = '', password: str = ''):
        self.base_urls = base_url.split(";")
        self.base_url = ""
        self.session = Session()

        if len(user) > 0:
            self.session.auth = (user, str(password if password is not None else ""),)
        else:
            self.session.auth = None

    def __str__(self):
        return "<Traefik Instance: {}>".format(self.base_urls)

    def __repr__(self):
        return self.__str__()

    def _get(self, method: str, params: dict = None):
        retr = Response()
        for base_url in self.base_urls:
            base_url = base_url.lstrip("/")
            try:
                retr = self.session.get(url="{}/{}".format(base_url, method), params=params)
                break
            except:
                pass
        return retr

    def _put(self, method: str, data):
        retr = Response()
        for base_url in self.base_urls:
            base_url = base_url.lstrip("/")
            try:
                retr = self.session.put(url="{}/{}".format(base_url, method), data=data)
                break
            except:
                pass
        return retr

    def health(self) -> dict:
        method = "health"
        retr = self._get(method)
        if retr.status_code == 200:
            return retr.json()
        else:
            return {"error": retr.status_code}

    def provider(self, provider: str = None) -> dict:
        method = "api/providers"
        if provider is not None:
            method = method + "/" + provider
        retr = self._get(method)
        if retr.status_code == 200:
            return retr.json()
        else:
            return {"error": retr.status_code}

    def put(self, provider: str = "rest", payload: dict = None):
        method = "api/providers/{}".format(provider)
        payload = json.dumps(payload)
        return self._put(method, data=payload)


class Payload:
    def __init__(self):
        pass

    def generate(self):
        return {}
