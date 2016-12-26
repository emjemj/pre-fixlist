from . import validator, prefixlist, dao
from time import sleep
from expandas.loader import RIPERESTLoader

class Updater:

    def __init__(self, config):
        self.config = config
        self.validator = None
        self.rpsl_objects = []

        if "validation" in config:
            self.validator = validator.Validator(config["validation"])
        else:
            self.validator = validator.Validator({})

        if "rpsl_objects" in config:
            self.rpsl_objects = config["rpsl_objects"]

        if "dao" in config:
            dao.DAO.setup(config["dao"]["class"], config["dao"])

    def run(self):
        loader = RIPERESTLoader()
        interval = self.config["global"]["interval"]

        while True:
            for rpsl_object in self.rpsl_objects:
                print("Fetching {}".format(rpsl_object))
                # Load data from routing registries
                as_set = loader.load_asset(rpsl_object)

                new = prefixlist.PrefixList.from_asset(as_set)

                # Use an empty list as the old one now.
                old = prefixlist.PrefixList(rpsl_object)

                self.validator.validate(new, old)
                new.debug()

            sleep(interval)
