import threading
import multiprocessing
from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
import time

#class WebServer(threading.Thread):
class WebServer(multiprocessing.Process):

    def __init__(self, port, app, queue):
       # threading.Thread.__init__(self)
        multiprocessing.Process.__init__(self)
        self.threadId = 2
        self.name = "pre-fixlist.WebServer"
        self.queue = queue

        self.server = HTTPServer(WSGIContainer(app))
        self.server.listen(port)
        self.exit = multiprocessing.Event()

    def run(self):
        IOLoop.instance().start()

        try:
            while not self.exit.is_set():
                sleep(1)
        finally:
            print("Finally!")
            IOLoop.instance().stop()
        


    def stop(self):
        print("Stopping webserver")
        self.exit.set()
