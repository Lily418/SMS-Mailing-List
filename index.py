import os
from flask import Flask, render_template, make_response, request, Response
from flask.ext.pymongo import PyMongo
import pusher


application= Flask("app18297361")
application.debug = True
application.config['PORT'] = 5000
application.config['MONGO_URI'] = os.getenv("MONGOHQ_URL", "mongodb://localhost:27017/sms-mailing-list")
mongo = PyMongo(application)

p = pusher.Pusher(
  app_id='54995',
  key='81830a54c2d8b0878390',
  secret='750dcc0203a9094075bc'
)


@application.route("/graph")
def showGraph():
    return render_template("landing.html")

def broadcastVote(vote):
    p['vote_channel'].trigger("vote_event", {"message" : vote})

@application.route('/', methods=['POST'])
def index():
    mongo.db.messages.insert({"from" : request.form['From'], "body" : request.form['Body']})
    broadcastVote(request.form['Body'])
    response = make_response(render_template("Response.xml", name=request.form['Body']))
    response.headers['Content-Type'] = "text/xml"
    return response

if __name__ == '__main__':
    application.run()
