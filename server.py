import threading
from App.init import init_app
from App.panel import run_web
from App.sync import run_sync

web = threading.Thread(target=run_web)
sync = threading.Thread(target=run_sync)

if __name__ == "__main__":
    init_app()

    web.start()
    sync.start()

    sync.join()
