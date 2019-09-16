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
@click.option('--entrypoint', default=os.getenv('TRAEFIK_ENTRYPOINT', '*'), help="Entrypoint to look for / filter on")
def run_server(refresh, dirname, url, user, password, entrypoint):
    dirname = str(dirname).lstrip('"').rstrip('"')
    url = str(url).lstrip('"').rstrip('"')
    user = str(user).lstrip('"').rstrip('"')
    password = str(password).lstrip('"').rstrip('"')

    while True:
        config = Config(os.path.normpath(dirname))
        output = Traefik(url, user, password)

        frontends = {}
        backends = {}
        rules = []

        for conf in config.instances:
            conf = config.get(conf)
            traefik = Traefik(conf.api.url, conf.api.user, conf.api.password)

            backends.update({
                conf.name: {
                    'loadBalancer': {'method': 'drr'},
                    'servers': {e.name: {'url': e.address, 'weight': 1} for e in conf.endpoints}
                }
            })

            providers = traefik.provider()
            providers = providers.values() if providers is not None else {}
            for provider in providers:
                if len(provider) > 0 and 'frontends' in provider.keys():
                    provider = provider['frontends']
                    for frontend, parameters in provider.items():
                        parameters['backend'] = conf.name
                        for route in parameters['routes'].values():
                            if route['rule'] in rules and str(route['rule']).startswith('Host'):
                                parameters['priority'] += (len([r for r in rules if r == route['rule']]) + 1)
                            rules.append(route['rule'])
                        if entrypoint == '*' or entrypoint in parameters['entryPoints']:
                            frontends.update({"{}-{}".format(conf.name, frontend.split("_")[-1]): parameters})

        payload = {'frontends': frontends, 'backends': backends}
        output.put(payload=payload)

        time.sleep(int(refresh))


if __name__ == '__main__':
    run_server()
