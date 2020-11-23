import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'RoadRnD',
      theme: ThemeData(
          primaryColor: Colors.white,
          textTheme: TextTheme(
            bodyText1: TextStyle(fontSize: 25.0, color: Colors.black),
          )),
      home: ListCars(),
    );
  }
}

class Car {
  final String brand;
  final String model;
  final String id;
  final String fuel_type;
  final int kms;
  final int num_of_seats;
  final String owner;
  final String year;

  Car(
      {this.brand,
      this.model,
      this.id,
      this.fuel_type,
      this.kms,
      this.num_of_seats,
      this.owner,
      this.year});

  factory Car.fromJson(Map<String, dynamic> json) {
    return Car(
        brand: json['Brand'],
        model: json['Model'],
        id: json['Id'],
        fuel_type: json['FuelType'],
        kms: json['Kms'],
        num_of_seats: json['Num_of_seats'],
        owner: json['Owner'],
        year: json['RegistrationYear']);
  }
}

Future<List<Car>> fetchCars() async {
  print("Getting cars");

  final response = await http.get('https://popular-donkey-97.loca.lt/cars');

  print(response.body);

  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    final json = jsonDecode(response.body);

    var car_list = new List<Car>();
    // The JSON data is an array, so the decoded json is a list.
    // We will do the loop through this list to parse objects.
    if (json != null) {
      json.forEach((element) {
        final car = Car.fromJson(element);
        print(car);
        car_list.add(car);
      });
    }

    return car_list;
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load album');
  }
}

class ListCars extends StatefulWidget {
  @override
  _ListCarsState createState() => _ListCarsState();
}

class _ListCarsState extends State<ListCars> {
  void updatePrice() {
    print(DateTime.now());
  }

  void goToCar(BuildContext context, Car car) {
    Navigator.of(context).push(MaterialPageRoute<void>(
      builder: (BuildContext context) {
        return Scaffold(
            appBar: AppBar(
              title: Text('${car.brand} ${car.model}'),
            ),
            body: Container(
                padding: const EdgeInsets.all(32),
                child: Column(
                  children: [
                    Expanded(
                        child: Column(
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                          Text(
                            "ID - ${car.id}",
                            style: Theme.of(context).textTheme.bodyText1,
                          ),
                          Text(
                            "Fuel - ${car.fuel_type}",
                            style: Theme.of(context).textTheme.bodyText1,
                          ),
                          Text(
                            "Kms - ${car.kms}",
                            style: Theme.of(context).textTheme.bodyText1,
                          ),
                          Text(
                            "Seats - ${car.num_of_seats}",
                            style: Theme.of(context).textTheme.bodyText1,
                          ),
                          Text(
                            "Year - ${car.year}",
                            style: Theme.of(context).textTheme.bodyText1,
                          ),
                          Text(
                            "Owner - ${car.owner}",
                            style: Theme.of(context).textTheme.bodyText1,
                          )
                        ])),
                    OutlineButton(
                        textColor: Color(0xFF6200EE),
                        highlightedBorderColor: Colors.black.withOpacity(0.12),
                        onPressed: () {
                          print('Unlock Car - ${car.id}');
                          Timer.periodic(Duration(milliseconds: 500),
                              (Timer t) => updatePrice());
                        },
                        child: Text(
                          "Unlock",
                          style: Theme.of(context).textTheme.bodyText1,
                        ))
                  ],
                )));
      }, // ..
    ));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: Text('RoadRnD')),
        body: FutureBuilder(
            future: fetchCars(),
            builder: (BuildContext context, AsyncSnapshot<List<Car>> snapshot) {
              if (snapshot.hasData) {
                List<Car> cars = snapshot.data;
                return ListView(
                  children: cars
                      .map(
                        (Car car) => ListTile(
                          title: Text(car.brand),
                          subtitle: Text("${car.model}"),
                          onTap: () {
                            print('Taped');
                            goToCar(context, car);
                          },
                        ),
                      )
                      .toList(),
                );
              } else {
                return Center(child: CircularProgressIndicator());
              }
            }));
  }
}
