import os
from flask import Flask, render_template, make_response, request
from flask.ext.pymongo import PyMongo

app = Flask("app18297361")
app.config['MONGO_URI'] = os.getenv("MONGOHQ_URL", "mongodb://localhost:27017/sms-mailing-list")
mongo = PyMongo(app)


@app.route('/', methods=['GET','POST'])
def index():
    mongo.db.messages.insert({"from" : request.args['From'], "body" : request.args['Body']})
    response = make_response(render_template("Response.xml"))
    response.headers['Content-Type'] = "text/xml"
    return response

if __name__ == '__main__':
    app.debug = True
    app.run()
