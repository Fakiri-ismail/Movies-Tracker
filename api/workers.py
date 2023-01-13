from uvicorn.workers import UvicornWorker

class MyUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        "log_config": "/home/ismail/Bureau/Movies_Tracker/logging.yaml",
    }