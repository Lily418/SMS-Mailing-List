import os
from flask import Flask, render_template, make_response, request
from flask.ext.pymongo import PyMongo
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from werkzeug.wsgi import SharedDataMiddleware
from socketio.server import SocketIOServer

class VoteNamespace(BaseNamespace):
    def onVote(self, msg):
        self.emit("vote", msg);

app = Flask("app18297361")
app.config['MONGO_URI'] = os.getenv("MONGOHQ_URL", "mongodb://localhost:27017/sms-mailing-list")
mongo = PyMongo(app)

@app.route("/graph")
def showGraph():
    return render_template("Graph.html")

@app.route("/socket.io/<path:path>")
def run_socketio(path):
    socketio_manage(request.environ, {'': VoteNamespace})

def broadcastVote(server, vote):
    pkt = {"type" : "event", "name" : "vote", "args" : {"vote" : vote}, "endpoint": "/Vote"}
    for sessid, socket in server.sockets.iteritems():
        socket.send_packet(pkt)


@app.route('/', methods=['GET','POST'])
def index():
    mongo.db.messages.insert({"from" : request.form['From'], "body" : request.form['Body']})
    broadcastVote(socketIOServer, request.form['Body'])
    response = make_response(render_template("Response.xml", name=request.form['Body']))
    response.headers['Content-Type'] = "text/xml"
    return response

if __name__ == '__main__':
    app = SharedDataMiddleware(app, {'/': os.path.join(os.path.dirname(__file__), 'static')})
    app.debug = True  
    global socketIOServer
    socketIOServer = SocketIOServer(('0.0.0.0', 8080), app, namespace="socket.io", policy_server=False)
    print('Listening on http://localhost:8080')
    socketIOServer.serve_forever()
