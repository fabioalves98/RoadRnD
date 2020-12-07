from flask import Flask, request, json, Response, render_template
from pymongo import MongoClient
import logging as log
import sys
from cryptography.fernet import Fernet
import jwt
import os
import datetime


app = Flask(__name__)
app.secret_key = os.urandom(12)
key = Fernet.generate_key()
f = Fernet(key)
authorization_codes = {}

def generate_authorization_code(client_id, redirect_url):
    message = json.dumps({
        "client_id": client_id,
        "redirect_url": redirect_url,
    }).encode()
    authorization_code = f.encrypt(message)

    authorization_codes[authorization_code] = {
        "client_id": client_id,
        "redirect_url": redirect_url
    }

    return authorization_code

def check_authorization_code(authorization_code, client_id, redirect_url):
    ac = authorization_codes.get(authorization_code)
    if not ac:
        return False

    client_id_ac = ac.get('client_id')
    redirect_url_ac = ac.get('redirect_url')

    if client_id != client_id_ac or redirect_url != redirect_url_ac:
        return False
    
    return True

def generate_access_token(client_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': client_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode_access_token(auth_token):
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        return payload['sub']
    except Exception as e:
        return e

@app.route('/')
def base():
    print('hello', file=sys.stdout)
    return render_template('index.html')

@app.route('/oauth/authorize', methods=['GET'])
def get_authorize():
    client_id = request.args.get('client_id')
    redirect_url = request.args.get('redirect_url')
    #code_challenge = request.args.get('code_challenge')
    client_id = "555555"
    return render_template('index.html', client_id = client_id, redirect_url = redirect_url)



@app.route('/oauth/login', methods=['POST'])
def post_success():
    data = request.values
    authorization_code = generate_authorization_code(data["client_id"], data["redirect_url"])

    print('Login success, client id ' + data["client_id"], file=sys.stdout)
    #####redirect??
    return Response(status=200)

@app.route('/oauth/token', methods = ['GET'])
def get_token():

    authorization_code = request.args.get('authorization_code')
    client_id = request.args.get('client_id')
    redirect_url = request.args.get('redirect_url')

    if None in [ authorization_code, client_id, redirect_url ]:
        return json.dumps({
            "error": "invalid_request"
        }), 400

    if  check_authorization_code(authorization_code, client_id, redirect_url):
        return json.dumps({
            "error": "access_denied"
        }), 400

    access_token = generate_access_token(client_id)
    response = json.dumps({ 
        "access_token": access_token,
        "token_type": "Bearer"
    })
    return Response(response=response,
                    status=200,
                    mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, port=5005, host='0.0.0.0')
    

    