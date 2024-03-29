from flask import Flask, request, json, Response
from pymongo import MongoClient
import logging as log
import requests

app = Flask(__name__)


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

        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]

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

    def update(self):
        log.info('Updating Data')
        filt = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, data):
        log.info('Deleting Data')
        #filt = data['Filter']
        response = self.collection.delete_one(data)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output

    def clear(self):
        output = self.collection.delete_many({})
        return output

    def findID(self, id):
        documents = self.collection.find({"id" : id})
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output
    def findFilters(self, fuel  , brand , model , year  , seats  ):
        query = {}
        if(fuel != None):
            query["fuelType"] = fuel
        if(brand != None):
            query["brand"] = brand
        if(model != None):
            query["model"] = model
        if(year != None):
            query["registrationYear"] = year
        if(seats != None):
            query["num_of_seats"] = seats
        #return query
        documents = self.collection.find(query)
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output


@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')

@app.route('/brands', methods=['GET'])
def get_brands():
    data = request.json
    try:
        access_token = data["access_token"]
    except:
        return Response(response=json.dumps({"Error" : "Please provide an access token and try again!!"}), 
                        status=400, 
                        mimetype='application/json')

    try:
        response = requests.get("http://roadrnd.westeurope.cloudapp.azure.com:5005/validate_token/" + access_token)
    except:
        return Response(response=json.dumps({"Error" : "There was a problem requesting the auth service!"}), 
                        status=500, 
                        mimetype='application/json')


    if response.status_code != 200:
        return Response(response=json.dumps({"Error" : "Access token invalid"}), 
                        status=400, 
                        mimetype='application/json')

    db = {
        "database" : "carInventory",
        "collection" : "cars"
    }
    obj1 = MongoAPI(db)
    response = obj1.read()
    brands = []
    for cars in response:
        if(cars["brand"] not in brands):
            brands.append(cars["brand"])
    return Response(response=json.dumps(brands),
                    status=200,
                    mimetype='application/json')


@app.route('/clean', methods=['GET'])
def get_clean():
    db = {
        "database" : "carInventory",
        "collection" : "cars"
    }
    obj1 = MongoAPI(db)
    response = obj1.clear()
    return Response(response=response,
                    status=200)

@app.route('/<brand>/models', methods=['GET'])
def get_models(brand):
    data = request.json
    try:
        access_token = data["access_token"]
    except:
        return Response(response=json.dumps({"Error" : "Please provide an access token and try again!!"}), 
                        status=400, 
                        mimetype='application/json')

    try:
        response = requests.get("http://roadrnd.westeurope.cloudapp.azure.com:5005/validate_token/" + access_token)
    except:
        return Response(response=json.dumps({"Error" : "There was a problem requesting the auth service!"}), 
                        status=500, 
                        mimetype='application/json')


    if response.status_code != 200:
        return Response(response=json.dumps({"Error" : "Access token invalid"}), 
                        status=400, 
                        mimetype='application/json')
    db = {
        "database" : "carInventory",
        "collection" : "cars"
    }
    obj1 = MongoAPI(db)
    response = obj1.findFilters( None  , brand , None , None  , None)
    if(len(response) > 0):
        models = []
        for cars in response:
            if(cars["model"] not in models):
                models.append(cars["model"])
        return Response(response=json.dumps(models),
                        status=200,
                        mimetype='application/json')
    return Response(response=json.dumps("Not found"),
                        status=404,
                        mimetype='application/json')

@app.route('/car/findByFilters', methods=['GET'])
def get_cars_by_filters():
    data = request.json
    try:
        access_token = data["access_token"]
    except:
        return Response(response=json.dumps({"Error" : "Please provide an access token and try again!!"}), 
                        status=400, 
                        mimetype='application/json')

    try:
        response = requests.get("http://roadrnd.westeurope.cloudapp.azure.com:5005/validate_token/" + access_token)
    except:
        return Response(response=json.dumps({"Error" : "There was a problem requesting the auth service!"}), 
                        status=500, 
                        mimetype='application/json')


    if response.status_code != 200:
        return Response(response=json.dumps({"Error" : "Access token invalid"}), 
                        status=400, 
                        mimetype='application/json')
    fuel = ''
    brand = ''
    model = ''
    year = ''
    seats = ''
    try:
        fuel = request.args.get('fuel')
    except:
        pass
    try:
        brand = request.args.get('brand')
    except:
        pass
    try:
        model = request.args.get('model')
    except:
        pass
    try:
        year = request.args.get('year')
    except:
        pass
    try:
        seats = request.args.get('seats')
    except:
        pass

    db = {
        "database" : "carInventory",
        "collection" : "cars"
    }
    obj1 = MongoAPI(db)
    response = obj1.findFilters( fuel  , brand , model , year  , seats)
    if(len(response) > 0):
        return Response(response=json.dumps(response),
                        status=200,
                        mimetype='application/json')
    return Response(response=json.dumps("Not found"),
                        status=404,
                        mimetype='application/json')



@app.route('/car/<carId>', methods=['GET'])
def get_car_byID(carId):
    data = request.json
    try:
        access_token = data["access_token"]
    except:
        return Response(response=json.dumps({"Error" : "Please provide an access token and try again!!"}), 
                        status=400, 
                        mimetype='application/json')

    try:
        response = requests.get("http://roadrnd.westeurope.cloudapp.azure.com:5005/validate_token/" + access_token)
    except:
        return Response(response=json.dumps({"Error" : "There was a problem requesting the auth service!"}), 
                        status=500, 
                        mimetype='application/json')


    if response.status_code != 200:
        return Response(response=json.dumps({"Error" : "Access token invalid"}), 
                        status=400, 
                        mimetype='application/json')
    car = {
    "id": "AB-50-DS",
    "brand": "Opel",
    "model": "Astra",
    "kms": 0,
    "registrationYear": "string",
    "fuelType": "gasoline",
    "owner": "Homer Simpson",
    "photo" : None,
    "num_of_seats": 5
    }
    db = {
        "database" : "carInventory",
        "collection" : "cars"
    }
    obj1 = MongoAPI(db)
    response = obj1.findID(carId)
    if(len(response) > 0):
        return Response(response=json.dumps(response),
                        status=200,
                        mimetype='application/json')
    return Response(response=json.dumps("Not found"),
                        status=404,
                        mimetype='application/json')




@app.route('/car', methods=['GET'])
def get_all_cars():
    data = request.json
    try:
        access_token = data["access_token"]
    except:
        return Response(response=json.dumps({"Error" : "Please provide an access token and try again!!"}), 
                        status=400, 
                        mimetype='application/json')

    try:
        response = requests.get("http://roadrnd.westeurope.cloudapp.azure.com:5005/validate_token/" + access_token)
    except:
        return Response(response=json.dumps({"Error" : "There was a problem requesting the auth service!"}), 
                        status=500, 
                        mimetype='application/json')


    if response.status_code != 200:
        return Response(response=json.dumps({"Error" : "Access token invalid"}), 
                        status=400, 
                        mimetype='application/json')
    db = {
        "database" : "carInventory",
        "collection" : "cars"
    }
    obj1 = MongoAPI(db)
    response = obj1.read()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app.route('/car', methods=['POST'])
def post_car():
    data = request.json
    db = {
        "database" : "carInventory",
        "collection" : "cars"
    }
    obj1 = MongoAPI(db)
    unique = obj1.findID(data["id"])
    if(len(unique) > 0):
        return Response(response=json.dumps("Car already in DB"),
                    status=403,
                    mimetype='application/json')
    doc = {"Document" : data}
    response = obj1.write(doc)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app.route('/car/<carId>', methods=['DELETE'])
def delete_car(carId):
    db = {
        "database" : "carInventory",
        "collection" : "cars"
    }
    obj1 = MongoAPI(db)
    response = obj1.delete({"id": carId})
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app.route('/mongodb', methods=['GET'])
def mongo_read():
    data = request.json
    db = {
        "database" : "carInventory",
        "collection" : "cars"
    }
    obj1 = MongoAPI(db)
    response = obj1.read()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app.route('/mongodb', methods=['POST'])
def mongo_write():
    data = request.json
    db = {
        "database" : "carInventory",
        "collection" : "cars"
    }
    obj1 = MongoAPI(db)
    response = obj1.write(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')
@app.route('/mongodb', methods=['PUT'])
def mongo_update():
    data = request.json
    if data is None or data == {} or 'Filter' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.update()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app.route('/mongodb', methods=['DELETE'])
def mongo_delete():
    data = request.json
    if data is None or data == {} or 'Filter' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.delete(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
    

    