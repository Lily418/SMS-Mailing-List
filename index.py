import os
from flask import Flask, render_template, make_response, request, Response
from flask.ext.pymongo import PyMongo
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from werkzeug.wsgi import SharedDataMiddleware
from socketio.server import SocketIOServer
from werkzeug.debug import DebuggedApplication
from gevent import monkey

monkey.patch_all()

class VoteNamespace(BaseNamespace):
    def initialize(self):
        self.logger = application.logger
        self.log("Socketio session started")
        
    def onVote(self, msg):
        self.emit("vote", msg);
        
    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def recv_connect(self):
        self.log("New connection")

    def recv_disconnect(self):
        self.log("Client disconnected")

application= Flask("app18297361")
application.debug = True
application.config['PORT'] = 5000
application.config['MONGO_URI'] = os.getenv("MONGOHQ_URL", "mongodb://localhost:27017/sms-mailing-list")
mongo = PyMongo(application)
socketIOServer = SocketIOServer(('', application.config['PORT']), application ,resource="socket.io")



@application.route("/broken")
def beBroken():
    pass

@application.route("/graph")
def showGraph():
    return render_template("landing.html")

@application.route('/socket.io/<path:remaining>')
def socketio(remaining):
    try:
        socketio_manage(request.environ, {'/vote': VoteNamespace}, request)
    except:
        application.logger.error("Exception while handling socketio connection",
                         exc_info=True)
    return Response()

def broadcastVote(server, vote):
    pkt = {"type" : "event", "name" : "vote", "args" : {"vote" : vote}, "endpoint": "/vote"}
    for sessid, socket in server.sockets.iteritems():
        socket.send_packet(pkt)


@application.route('/', methods=['GET','POST'])
def index():
    mongo.db.messages.insert({"from" : request.form['From'], "body" : request.form['Body']})
    broadcastVote(socketIOServer, request.form['Body'])
    response = make_response(render_template("Response.xml", name=request.form['Body']))
    response.headers['Content-Type'] = "text/xml"
    return response

if __name__ == '__main__':
    print('Listening on http://localhost:' + str(application.config['PORT']))
    socketIOServer.serve_forever()
