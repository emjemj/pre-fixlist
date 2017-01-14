from . import validator, prefixlist, dao
from time import sleep
from expandas.loader import RIPERESTLoader
import threading
import multiprocessing

#class UpdaterWorker(threading.Thread):
class UpdaterWorker(multiprocessing.Process):
    def __init__(self, rpsl_objects, queue):
        #threading.Thread.__init__(self)
        multiprocessing.Process.__init__(self)
        self.queue = queue
        #self.threadId = 1
        #self.name = "pre-fixlist.UpdaterWorker"
        #self.validator = validator
        self.rpsl_objects = rpsl_objects
        #self.loader = RIPERESTLoader()
        self.interval = 300
        self.exit = multiprocessing.Event() 

    def run(self):
        while not self.exit.is_set():
            print(".")
            for rpsl_object in self.rpsl_objects:
                self.queue.put(rpsl_object)
                
    #            print("Fetching {}".format(rpsl_object))
    #            as_set = self.loader.load_asset(rpsl_object)
    #            new = prefixlist.PrefixList.from_asset(as_set)
    #            old = prefixlist.PrefixList(rpsl_object)
    #            self.validator.validate(new, old)
    #            new.debug()
            sleep(self.interval)
        print("Running = False")

    def stop(self):
        print("Stopping")
        self.exit.set()
