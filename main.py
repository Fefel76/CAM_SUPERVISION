#import cv2
from flask import Flask, render_template, request
#import requests
#from requests.exceptions import HTTPError
app= Flask(__name__)

@app.route("/")
def hello():

    return render_template('index.html')

app.run(debug=True, host="0.0.0.0")
