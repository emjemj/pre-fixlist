import multiprocessing
from . import prefixlist, dao
from expandas.loader import RIPERESTLoader
import queue
import logging

class Worker(multiprocessing.Process):
    def __init__(self, queue, validator):
        super().__init__() 
        self.queue = queue
        self.validator = validator
        self.loader = RIPERESTLoader()
        self.exit = multiprocessing.Event()

    def run(self):
        while not self.exit.is_set():
            try:
                item = self.queue.get(True, 5)
            except queue.Empty:
                # No item from queue, try again
                continue

            logging.info("Working on %s", item)

            as_set = self.loader.load_asset(item)
            new = prefixlist.PrefixList.from_asset(as_set)
            old = prefixlist.PrefixList(item)

            self.validator.validate(new, old)
            new.debug()
        logging.info("Worker stopped")

    def stop(self):
        logging.info("Stopping worker")
        self.exit.set()
