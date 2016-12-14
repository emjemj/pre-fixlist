from . import validator
from time import sleep
from expandas.loader import RIPERESTLoader

class Updater:

    def __init__(self, config):
        self.config = config
        self.validator = None
        self.sources = []

        if "validation" in config:
            self.validator = validator.Validator(config["validation"])

        if "sources" in config:
            self.sources = config["sources"]

    def run(self):
        loader = RIPERESTLoader()
        interval = self.config["global"]["interval"]

        while True:
            for source in self.sources:
                print("Fetching {}".format(source))
                asset = loader.load_asset(source)
                validated = self.validate(asset)
                for v in validated:
                    print("{}: {}".format(v["member"], v["action"]))
                denied = [ e for e in validated if e["action"] == "deny" ]
                print("{} denied entries in {}".format(len(denied), asset))

            sleep(interval)

    def validate(self, asset):
        result = []
        if self.validator is None:
            for member in asset:
                # Default permit if no validators are specified
                result.append({"member": member, "action": "permit" })
        else:
            result = self.validator.validate(asset)
        return result
