from gevent import monkey
from flask import Flask, Response, render_template, request
from socketio import socketio_manage
from socketio.namespace import BaseNamespace

monkey.patch_all()

application = Flask(__name__)
application.debug = True
application.config['PORT'] = 5000

class ChatNamespace(BaseNamespace):
    def initialize(self):
        self.logger = application.logger
        self.log("Socketio session started")

    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def recv_connect(self):
        self.log("New connection")

    def recv_disconnect(self):
        self.log("Client disconnected")
        

@application.route('/', methods=['GET'])
def landing():
    return render_template('landing.html')

@application.route('/socket.io/<path:remaining>')
def socketio(remaining):
    try:
        socketio_manage(request.environ, {'/chat': ChatNamespace}, request)
    except:
        application.logger.error("Exception while handling socketio connection",
                         exc_info=True)
    return Response()