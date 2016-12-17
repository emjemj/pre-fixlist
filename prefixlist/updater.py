from . import validator, prefixlist
from time import sleep
from expandas.loader import RIPERESTLoader

class Updater:

    def __init__(self, config):
        self.config = config
        self.validator = None
        self.sources = []

        if "validation" in config:
            self.validator = validator.Validator(config["validation"])
        else:
            self.validator = validator.Validator({})

        if "sources" in config:
            self.sources = config["sources"]

    def run(self):
        loader = RIPERESTLoader()
        interval = self.config["global"]["interval"]

        while True:
            for source in self.sources:
                print("Fetching {}".format(source))
                # Load data from routing registries
                asset = loader.load_asset(source)

                new = prefixlist.PrefixList.from_asset(asset)

                # Use an empty list as the old one now.
                old = prefixlist.PrefixList(asset.name)

                self.validator.validate(new, old)
                new.debug()

            sleep(interval)
