from requests import Session


class Traefik:
    def __init__(self, base_url: str, user: str = '', password: str = ''):
        self.base_url = base_url.lstrip("/")
        self.session = Session()

        if len(user) > 0:
            self._auth = (user, password,)
        else:
            self._auth = None

    def _get(self, method: str, params: dict = None):
        return self.session.get(url="{}/{}".format(self.base_url, method), params=params, auth=self._auth)
