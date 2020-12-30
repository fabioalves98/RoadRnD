import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:road_rnd_app/carview.dart';
import 'dart:convert';

import 'global.dart';
import 'car.dart';

Future<List<Car>> fetchCars() async {
  print("Getting cars");

  final response = await http.get(Global.lt_link + '/cars');

  print(response.body);

  if (response.statusCode == 200) {
    final json = jsonDecode(response.body);

    var car_list = new List<Car>();

    if (json != null) {
      json.forEach((element) {
        final car = Car.fromJson(element);
        print(car);
        car_list.add(car);
      });
    }

    return car_list;
  } else {
    throw Exception('Failed to load car list');
  }
}

class ListCars extends StatefulWidget {
  @override
  _ListCarsState createState() => _ListCarsState();
}

class _ListCarsState extends State<ListCars> {
  void goToCar(BuildContext context, Car car) {
    Navigator.of(context).push(MaterialPageRoute<void>(
      builder: (BuildContext context) {
        return CarView(car: car);
      }, // ..
    ));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
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
