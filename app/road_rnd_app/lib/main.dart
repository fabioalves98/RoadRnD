import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'RoadRnD',
      theme: ThemeData(
        primaryColor: Colors.white,
      ),
      home: ListCars(),
    );
  }
}

class Car {
  final String brand;
  final String model;
  final String id;

  Car({this.brand, this.model, this.id});

  factory Car.fromJson(Map<String, dynamic> json) {
    return Car(
      brand: json['Brand'],
      model: json['Model'],
      id: json['Id'],
    );
  }
}

Future<List<Car>> fetchCars() async {
  print("Getting cars");

  final response = await http.get('https://36fc9bc9d525.ngrok.io/cars');

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
  final _cars = <String>['Honda', 'Chevrolet', 'BMW'];
  final _biggerFont = TextStyle(fontSize: 18.0);

  Widget _buildSuggestions() {
    return ListView.separated(
      padding: EdgeInsets.all(16.0),
      itemCount: 4,
      itemBuilder: /*1*/ (context, index) {
        return _buildRow(_cars[index]);
      },
      separatorBuilder: (BuildContext context, int index) => const Divider(),
    );
  }

  Widget _buildRow(String pair) {
    return ListTile(
      title: Text(
        pair,
        style: _biggerFont,
      ),
      onTap: () {
        print('Taped');
      },
    );
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
                            subtitle: Text("${car.model}")),
                      )
                      .toList(),
                );
              } else {
                return Center(child: CircularProgressIndicator());
              }
            }));
  }
}
