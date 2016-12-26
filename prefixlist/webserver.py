import threading
from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop

class WebServer(threading.Thread):

    def __init__(self, port, app):
        threading.Thread.__init__(self)
        self.threadId = 2
        self.name = "pre-fixlist.WebServer"

        self.server = HTTPServer(WSGIContainer(app))
        self.server.listen(port)

    def run(self):
        IOLoop.instance().start()
