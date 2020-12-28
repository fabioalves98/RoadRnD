from flask import Flask, request, json, Response, render_template, redirect
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
clients = []

class MongoAPI:
    def __init__(self, data):
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s:\n%(message)s\n')
        # self.client = MongoClient("mongodb://localhost:27017/")  # When only Mongo DB is running on Docker.
        self.client = MongoClient("mongodb://mymongo_1:27017/")     # When both Mongo and This application is running on
                                                                    # Docker and we are using Docker Compose

        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def read(self):
        log.info('Reading All Data')
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def write(self, data):
        log.info('Writing Data')
        new_document = data["Document"]
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output


    def upsert(self, filt, data):
        log.info('Updating Data')
        #options = { "upsert": true }
        updated_data = {"$set": data}
        response = self.collection.update_one(filt, updated_data, upsert=True)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def update(self):
        log.info('Updating Data')
        filt = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, data):
        log.info('Deleting Data')
        response = self.collection.delete_one(data)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output

    def findAuth_Code(self, auth_c):
        documents = self.collection.find({"auth_code" : auth_c})
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output
    def findId(self, id):
        documents = self.collection.find({"client_id" : id})
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

def generate_authorization_code(client_id, redirect_url, user_id):
    message = json.dumps({
        "client_id": client_id,
        "redirect_url": redirect_url,
        "user_id": user_id
    }).encode()
    authorization_code = f.encrypt(message).decode("utf-8")
    db = {
        "database" : "auth",
        "collection" : "authCodes"
    }
    obj1 = MongoAPI(db)
    data = {
        "auth_code": authorization_code,
        "client_id": client_id,
        "redirect_url": redirect_url,
        "user_id": user_id
    }

    doc = {"Document" : data}
    response = obj1.upsert({"user_id" :user_id }, data)

    # authorization_codes[authorization_code] = {
    #     "client_id": client_id,
    #     "redirect_url": redirect_url
    # }

    return authorization_code

def check_authorization_code(authorization_code, client_id, redirect_url):
    db = {
        "database" : "auth",
        "collection" : "authCodes"
    }
    obj1 = MongoAPI(db)
    ac = obj1.findAuth_Code(authorization_code)
    log.info('ac ' + str(ac))
    #ac = authorization_codes.get(authorization_code )
    if len(ac) == 0:
        return False

    #client_id_ac = ac.get('client_id')
    #redirect_url_ac = ac.get('redirect_url')
    client_id_ac = ac[0]['client_id']
    redirect_url_ac = ac[0]['redirect_url']

    if client_id != client_id_ac or redirect_url != redirect_url_ac:
        return False
    
    return True


#https://realpython.com/token-based-authentication-with-flask/#encode-token

def generate_access_token(client_id):
    # db = {
    #     "database" : "auth",
    #     "collection" : "authCodes"
    # }
    # obj1 = MongoAPI(db)
    # data = {
    #     "client_id": client_id
    # }

    # doc = {"Document" : data}
    # response = obj1.write(doc)
    #clients.append(client_id)
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
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

@app.route('/validate_token/<auth_token>', methods=['GET'])
def verify_access_token(auth_token):
    client_id = decode_access_token(auth_token)
    print('cliente_id_validate' + str(client_id), file=sys.stdout)

    db = {
        "database" : "auth",
        "collection" : "authCodes"
    }
    obj1 = MongoAPI(db)
    client = obj1.findId(client_id)

    #if client_id in clients:
    if len(client) > 0:
        return Response(response=json.dumps("OK"),
                        status=200,
                        mimetype='application/json')
    else:
        return Response(response=json.dumps("Bad Request"),
                        status=400,
                        mimetype='application/json')


def decode_access_token(auth_token):
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), algorithms='HS256')
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

@app.route('/')
def base():
    print('hello', file=sys.stdout)
    return render_template('index.html')

@app.route('/oauth/authorize', methods=['GET'])
def get_authorize():
    client_id = request.args.get('client_id')
    redirect_url = request.args.get('redirect_url')
    #code_challenge = request.args.get('code_challenge')
    return render_template('index.html', client_id = client_id, redirect_url = redirect_url)



@app.route('/oauth/login', methods=['POST'])
def post_success():
    data = request.values
    print('Login success, client id ' + str(data), file=sys.stdout)
    user_id = data['id']
    user_name = data['userName']
    image = data['image']
    mail = data['mail']
    authorization_code = generate_authorization_code(data["client_id"], data["redirect_url"], user_id)
    user_info = {
        "auth_code" : authorization_code,
        "client_id" : user_id,
        "user_name" : user_name,
        "image"     : image,
        "mail"      : mail
    }
    response = {
        "redirect_url" : data["redirect_url"],
        "user_info"     : user_info
    }

    #save in bd
    print('Login success, client id ' + json.dumps(user_info), file=sys.stdout)
    #####redirect?? com authorization_code e user_info
    #return render_template(authorization_code)
    #redirect_url = data["redirect_url"] + "?auth_code=" + authorization_code 
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')
    #return Response(response=json.dumps(user_info), status=200, mimetype='application/json')


@app.route('/oauth/token', methods = ['GET'])
def get_token():

    authorization_code = request.args.get('authorization_code')
    client_id = request.args.get('client_id')
    redirect_url = request.args.get('redirect_url')

    if None in [ authorization_code, client_id, redirect_url ]:
        return Response(response=json.dumps({"error": "invalid_request"}),
                        status=400,
                        mimetype='application/json')

    if not check_authorization_code(authorization_code, client_id, redirect_url):
        return Response(response=json.dumps({"error": "access_denied"}),
                        status=400,
                        mimetype='application/json')

    access_token = generate_access_token(client_id)
    response = json.dumps({ 
        "access_token": access_token.decode("utf-8"),
        "token_type": "Bearer"
    })
    return Response(response=response,
                    status=200,
                    mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, port=5005, host='0.0.0.0')
    

    