import os
from flask import Flask, render_template, make_response, request
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv("MONGOHQ_URL", "mongodb://localhost:27017/sms-mailing-list")
mongo = PyMongo(app)


@app.route('/', methods=['GET','POST'])
def index():
    mongo.db.messages.insert(request.args)
    response = make_response(render_template("Response.xml"))
    response.headers['Content-Type'] = "text/xml"
    return response

