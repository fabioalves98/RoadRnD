from flask import Flask, request, json, Response, render_template
from pymongo import MongoClient
import logging as log

app = Flask(__name__)

@app.route('/')
def base():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5005, host='0.0.0.0')
    

    