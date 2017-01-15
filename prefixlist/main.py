from multiprocessing import Queue
from . import dao, validator, webserver, updater, api, worker
import yaml

class PrefixListMain:

    updaterThread = None
    webServerThread = None
    workers = []

    def __init__(self, configfile):

        with open(configfile, "r") as stream:
            config = yaml.load(stream)

        if "dao" in config:
            # Start database abstraction layer
            dao.DAO.setup(config["dao"]["class"], config["dao"])
        else:
            raise ValueError("Please configure a DAO")

        if "validation" in config:
            validation = config["validation"]
        else: 
            validation = {}

        self.validator = validator.Validator(validation)

        if "rpsl_objects" in config:
            self.rpsl_objects = config["rpsl_objects"]

        self.config = config

        self.queue = Queue()

        self.updaterThread = updater.UpdaterWorker(self.rpsl_objects, self.queue)
        self.webServerThread = webserver.WebServer(5000, api.app, self.queue)

        for i in range(0,1):
            wrk = worker.Worker(self.queue, self.validator)
            wrk.start()
            self.workers.append(wrk)

        self.updaterThread.start()
        self.webServerThread.start()

    def stop(self):
        print("Stopping the show")
        self.updaterThread.stop()
        self.webServerThread.stop()

        for w in self.workers:
            w.stop()

        print("Show stopped")
