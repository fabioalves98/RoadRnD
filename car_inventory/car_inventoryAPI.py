from flask import Flask, request, json, Response
from pymongo import MongoClient
import logging as log

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

    def read(self):
        log.info('Reading All Data')
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def write(self, data):
        log.info('Writing Data')
        new_document = data['Document']
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
        filt = data['Filter']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output


@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "DOWN"}),
                    status=200,
                    mimetype='application/json')

@app.route('/brands', methods=['GET'])
def get_brands():
    response = ['Audi', 'BMW', 'Opel' ]
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/<brand>/models', methods=['GET'])
def get_models(brand):
    if(brand == 'opel'):
        response = ['Corsa', 'Astra']
        return Response(response=json.dumps(response),
                        status=200,
                        mimetype='application/json') 
    response = ['A4', 'A3', 'A7' ]
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/car/findByFilters', methods=['GET'])
def get_cars_by_filters():
    fuel = ''
    brand = ''
    model = ''
    year = ''
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

    car1 = {
    "id": "AB-56-DS",
    "brand": "Kia",
    "model": "Ceed",
    "kms": 0,
    "registrationYear": "string",
    "fuelType": "gasoline",
    "owner": "Homer Simpson",
    "photo" : None
    }
    car2 = {
    "id": "AB-50-DS",
    "brand": "Opel",
    "model": "Astra",
    "kms": 0,
    "registrationYear": "string",
    "fuelType": "gasoline",
    "owner": "Homer Simpson",
    "photo" : None
    }
    return Response(response=json.dumps([car1, car2]),
                    status=200,
                    mimetype='application/json')


@app.route('/car/<carId>', methods=['GET'])
def get_car_byID(carId):
    car = {
    "id": "AB-50-DS",
    "brand": "Opel",
    "model": "Astra",
    "kms": 0,
    "registrationYear": "string",
    "fuelType": "gasoline",
    "owner": "Homer Simpson",
    "photo" : None
    }
    return Response(response=json.dumps(car),
                    status=200,
                    mimetype='application/json')


@app.route('/car', methods=['GET'])
def get_all_cars():

    car1 = {
    "id": "AB-56-DS",
    "brand": "Kia",
    "model": "Ceed",
    "kms": 0,
    "registrationYear": "string",
    "fuelType": "gasoline",
    "owner": "Homer Simpson",
    "photo" : None
    }
    car2 = {
    "id": "AB-50-DS",
    "brand": "Opel",
    "model": "Astra",
    "kms": 0,
    "registrationYear": "string",
    "fuelType": "gasoline",
    "owner": "Homer Simpson",
    "photo" : None
    }
    return Response(response=json.dumps([car1, car2]),
                    status=200,
                    mimetype='application/json')

@app.route('/mongodb', methods=['GET'])
def mongo_read():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.read()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app.route('/mongodb', methods=['POST'])
def mongo_write():
    data = request.json
    if data is None or data == {} or 'Document' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
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