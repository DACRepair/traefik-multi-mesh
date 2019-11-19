from App.Common.storage import base
from App.Model import *


def init_app():
    return base.metadata.create_all()
