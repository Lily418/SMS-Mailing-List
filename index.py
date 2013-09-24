import os
from flask import Flask, render_template, make_response

app = Flask(__name__)

@app.route('/')
def index():
    response = make_response(render_template("Response.xml"))
    response.headers['content-type'] = "text/xml"
    return render_template("Response.xml")

