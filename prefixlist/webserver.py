import threading
import multiprocessing
from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
import time
import logging

class WebServer(multiprocessing.Process):

    def __init__(self, port, api, queue):
        super().__init__()
        self.threadId = 2
        self.name = "pre-fixlist.WebServer"
        self.queue = queue
        self.ioloop = IOLoop.instance()
        api.queue = queue

        self.server = HTTPServer(WSGIContainer(api.app))
        self.server.listen(port)
        self.exit = multiprocessing.Event()

    def run(self):
        self.ioloop.start()

    def stop(self):
        logging.info("Stopping webserver")
        self.server.stop()
        self.ioloop.stop()
        # This can probably be done in a neater way
        self.terminate()
        logging.info("Stopped webserver")
