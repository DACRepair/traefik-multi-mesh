import click
import os
import time
from App.Common.Config import Config
from App.Traefik.TraefikAPI import Traefik


@click.command()
@click.option('--refresh', default=os.getenv("APP_REFRESH", 10), help="Refresh speed (seconds).")
@click.option('--dirname', default=os.getenv("APP_CONFIG", "./config.d"), help="Config directory to scan.")
@click.option('--url', default=os.getenv("TRAEFIK_URL", "http://127.0.0.1:8080"), help="Traefik Output Node Base URL")
@click.option('--user', default=os.getenv("TRAEFIK_USER", ""), help="Traefik Output Node Auth Username")
@click.option('--password', default=os.getenv("TRAEFIK_PASS", ""), help="Traefik Output Node Auth Password")
def run_server(refresh, dirname, url, user, password):
    refresh = int(refresh)
    dirname = str(dirname).lstrip('"').rstrip('"')
    url = str(url).lstrip('"').rstrip('"')
    user = str(user).lstrip('"').rstrip('"')
    password = str(password).lstrip('"').rstrip('"')

    output = Traefik(url, user, password)
    while True:
        config = Config(os.path.normpath(dirname))
        backends = {}
        frontends = {}
        routes = []
        for e in config.instances:
            cfg = config.get(e)
            backends[cfg.name] = {
                'loadBalancer': {'method': 'drr'},
                'servers': {s.name: {'url': s.address, 'weight': 1} for s in cfg.endpoints}
            }

            instance = Traefik(cfg.api.url, cfg.api.user, cfg.api.password)
            data = instance.provider()
            if data is not None:
                for key in data.keys():
                    if len(data[key].keys()) > 0:
                        for frontend, params in data[key]['frontends'].items():
                            frontend = "{}_{}".format(cfg.name, frontend)
                            if cfg.api.entrypoint in params['entryPoints'] or cfg.api.entrypoint == '*':
                                params['backend'] = cfg.name
                                frontends[frontend] = params
                                routes.extend([str(x['rule']).lower() for x in dict(params['routes']).values()])

        dupes = list(set([x for x in routes if routes.count(x) > 1]))
        if len(dupes) > 0:
            print("There are duplicate hostnames in the rules: {}".format(", ".join(dupes)))

        _frontends = {}
        for frontend, params in frontends.items():
            dupe = False
            for d in dupes:
                if d in str(params).lower():
                    dupe = True
            if not dupe:
                _frontends[frontend] = params
        frontends = _frontends

        payload = {'frontends': frontends, 'backends': backends}
        print(payload)
        output.put(payload=payload)

        time.sleep(int(refresh))


if __name__ == '__main__':
    run_server()
