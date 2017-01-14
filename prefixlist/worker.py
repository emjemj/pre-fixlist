import multiprocessing
from . import prefixlist, dao
from expandas.loader import RIPERESTLoader

class Worker(multiprocessing.Process):
    def __init__(self, queue, validator):
        super().__init__() 
        self.queue = queue
        self.validator = validator
        self.loader = RIPERESTLoader()
        self.exit = multiprocessing.Event()

    def run(self):
        while not self.exit.is_set():
            item = self.queue.get()
            print("Working on {}".format(item))

            as_set = self.loader.load_asset(item)
            new = prefixlist.PrefixList.from_asset(as_set)
            old = prefixlist.PrefixList(item)

            self.validator.validate(new, old)
            new.debug()
        print("Worker loop exited")

    def stop(self):
        print("Stopping worker")
        self.exit.set()
