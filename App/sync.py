import time
from App.Common.app import SyncServer
from App.Common.config import REFRESH_RATE


def run_sync():
    server = SyncServer()
    while True:
        error = 0
        if server.do_sync():
            error = 0
            time.sleep(REFRESH_RATE)
        else:
            error += 1
            time.sleep(REFRESH_RATE)
        if error < 3:
            exit(1)
