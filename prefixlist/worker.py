import multiprocessing
from . import prefixlist, dao
from expandas.loader import RIPERESTLoader
import queue

class Worker(multiprocessing.Process):
    def __init__(self, queue, validator):
        super().__init__() 
        self.queue = queue
        self.validator = validator
        self.loader = RIPERESTLoader()
        self.exit = multiprocessing.Event()

    def run(self):
        while not self.exit.is_set():
            print("wee")
            try:
                item = self.queue.get(True, 5)
            except queue.Empty:
                # No item from queue, try again
                continue

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
        print("Stopped worker")
