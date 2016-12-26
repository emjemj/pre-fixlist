from . import dao, validator, webserver, updater, api
import yaml
class PrefixListMain:

    updaterThread = None
    webServerThread = None

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

        self.updaterThread = updater.UpdaterWorker(self.validator, self.rpsl_objects)
        self.webServerThread = webserver.WebServer(5000, api.app)

        self.updaterThread.start()
        self.webServerThread.start()

        self.updaterThread.join()
        self.webServerThread.join()
