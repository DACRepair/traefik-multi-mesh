import os
from configparser import ConfigParser
from glob import glob


class Config:
    def __init__(self, conf_dir):
        self.conf_dir = os.path.normpath(conf_dir)
        confs = list(glob(conf_dir + "/*.ini"))
        self.confs = {}
        for conf in confs:
            data = ConfigParser()
            data.read(conf)
            self.confs[os.path.basename(conf).split(".")[0]] = {s: data.items(s) for s in data.sections()}
