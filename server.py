import pprint
from App.Common.Config import Config, Instance

config = Config("config.d")


def sync_instance(instance: Instance):
    return instance


for e in config.instances:
    sync_instance(config.get(e))
