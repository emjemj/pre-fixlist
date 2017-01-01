from . import validator, prefixlist, dao
from time import sleep
from expandas.loader import RIPERESTLoader
import threading

class UpdaterWorker(threading.Thread):
    def __init__(self, validator, rpsl_objects):
        threading.Thread.__init__(self)
        self.threadId = 1
        self.name = "pre-fixlist.UpdaterWorker"
        self.validator = validator
        self.rpsl_objects = rpsl_objects
        self.loader = RIPERESTLoader()
        self.interval = 300
        print(self)

    def run(self):
        while True:
            print(".")
            for rpsl_object in self.rpsl_objects:
                print("Fetching {}".format(rpsl_object))
                as_set = self.loader.load_asset(rpsl_object)
                new = prefixlist.PrefixList.from_asset(as_set)
                old = prefixlist.PrefixList(rpsl_object)
                self.validator.validate(new, old)
                new.debug()
            sleep(self.interval)
