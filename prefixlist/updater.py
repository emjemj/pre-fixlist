from . import validator, prefixlist, dao
import time
from expandas.loader import RIPERESTLoader
import multiprocessing
import logging

#class UpdaterWorker(threading.Thread):
class UpdaterWorker(multiprocessing.Process):
    def __init__(self, rpsl_objects, queue):
        super().__init__()
        self.queue = queue
        self.rpsl_objects = rpsl_objects
        self.interval = 300
        self.exit = multiprocessing.Event() 
        self.last_run = 0

    def run(self):
        while not self.exit.is_set():
            time.sleep(1)
            logging.debug("Last run: %d, next run: %d, now: %d", self.last_run, self.last_run + self.interval, int(time.time()))
            if (self.last_run > 0) and ((self.last_run + self.interval) > int(time.time())):
                continue
            for rpsl_object in self.rpsl_objects:
                self.queue.put(rpsl_object)
            self.last_run = int(time.time())
        logging.info("Scheduler loop exited")

    def stop(self):
        logging.info("Stopping work scheduler")
        self.exit.set()
