import os
from flask import Flask, render_template, make_response

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    response = make_response(render_template("Response.xml"))
    response.headers['Content-Type'] = "text/xml"
    return response

