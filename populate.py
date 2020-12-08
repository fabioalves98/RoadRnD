import sys
import string
import random
import requests
import json

from bs4 import BeautifulSoup
import urllib3

# API_LINK = "http://localhost" 
API_LINK = "http://40.115.31.209"

cars = {
    'Honda' :   ['Civic', 'Accord', 'Brio', 'City', 'Jazz', 'Legend'],
    'Kia'   :   ['Ceed', 'Rio', 'Stinger', 'Soul'],
    'Renault':  ['Clio', 'Laguna', 'Megane', 'Scenic', 'Twingo', 'Alpine', 'Zoe'],
    'Mazda':    ['RX-8', 'RX-7', 'CX-9', '6', '3'],
    'BMW'   :   ['X7', 'M5', 'Z4', 'I8', 'M3', 'X1'],
    'Audi'  :   ['A5', 'Q7', 'A7', 'A8', 'A4', 'R8'],
    'Toyota':   ['Prius', 'Corolla', 'Yaris', 'Supra'],
    'Ford'  :   ['Transit', 'Focus', 'Fiesta', 'GT350'],
    'Volvo':    ['V40', 'XC60', 'XC40', 'S60', 'V70']
}

first_name = ['James', 'John', 'Robert', 'David', 'Daniel', 'Mary',  'Barbara', 'Susan', 'Jessica', 'Sandra']
last_name = ['Smith', 'Williams', 'Garcia', 'Wilson', 'Martin', 'Harris', 'Turner', 'Parker' ]
fuel_type = ['gasoline', 'diesel', 'LPG', 'eletric', 'hybrid']
num_of_seatsOP = [2, 4, 5, 7]

tags = ['tag1', 'tagX', 'tagV2']
locationAveiro = [40.640802, -8.653285]
status_options = ['Rented', 'Parked']
#location

for x in range(30):
    s = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    car_id = s[0:2] + '-'+ s[2:4] + '-' + s[4:6]
    brand = random.choice(list(cars))
    model = random.choice(cars[brand])
    kms = random.randint(50000, 400000)
    registrationYear = random.randint(2000, 2020)
    fuelType = random.choice(fuel_type)
    owner = random.choice(first_name) + ' ' + random.choice(last_name)
    
    #get url photo
    http = urllib3.PoolManager()
    url = "https://www.google.com/images?q=" + brand + "+" + model
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, features="lxml")
    images = soup.findAll('img')
    photo = images[1].get('src')

    num_of_seats = random.choice(num_of_seatsOP)
    price_per_minute = random.randint(1, 10)
    car = {
        "id": car_id,
        "brand": brand,
        "model": model,
        "kms": kms,
        "registrationYear": str(registrationYear),
        "fuelType": fuelType,
        "owner": owner,
        "photo" : photo,
        "num_of_seats": num_of_seats,
        "price_per_minute": price_per_minute
    }

    #tag = random.choice(tags)
    tag = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    status = random.choice(status_options)

    location = str(locationAveiro[0] + random.randint(-100, 100)*0.0001) + ', ' + str(locationAveiro[1] + random.randint(-100, 100)*0.0001)
    #print(car)
    #Car inventory service
    print("Add car to inventory service")
    API_URL = API_LINK + ":5001/car"
    headers = {"Content-Type": "application/json"}
    response = requests.post(API_URL, data = json.dumps(car),headers=headers )
    print(response)
    if(response.status_code == 200):
        # #Unlock service
        print("Add car to unlock service")
        API_URL = API_LINK + ":5003/add"
        headers = {"Content-Type": "application/json"}
        data = {
            "id": car_id,
            "tag": tag
        }
        response = requests.post(API_URL, data = json.dumps(data),headers=headers )
        print(response)

        #Car location service
        print("Add car to location service")
        API_URL = API_LINK + ":5002/car/" + str(car_id)
        headers = {"Content-Type": "application/json"}
        data = {
            "location": location,
            "status": status
        }
        response = requests.post(API_URL, data = json.dumps(data),headers=headers )
        print(response)
    


