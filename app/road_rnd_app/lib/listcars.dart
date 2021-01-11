import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import 'global.dart';
import 'car_view.dart';
import 'car.dart';
import 'dropdown.dart';

Future<List<Car>> fetchCars() async {
  print("Getting cars");

  final response = await http
      .get(Global.lt_link + '/cars', headers: {"Authorization": Global.token});

  print(response.body);

  if (response.statusCode == 200) {
    final json = jsonDecode(response.body);

    List<Car> carList = [];

    if (json != null) {
      json.forEach((element) {
        carList.add(Car.fromJson(element));
      });
    }

    return carList;
  } else {
    throw Exception('Failed to load car list');
  }
}

class ListCars extends StatefulWidget {
  @override
  _ListCarsState createState() => _ListCarsState();
}

class _ListCarsState extends State<ListCars> {
  List<String> fuelFilterItems = [
    "Gasoline",
    "Diesel",
    "GPL",
    "Electric",
    "Hybrid"
  ];
  List<DropdownMenuItem<String>> fuelDropDown;
  String fuelSelected;

  List<DropdownMenuItem<String>> buildDropDown(List listItems) {
    List<DropdownMenuItem<String>> items = [];
    for (String listItem in listItems) {
      items.add(
        DropdownMenuItem(
          child: Text(listItem),
          value: listItem,
        ),
      );
    }
    return items;
  }

  Widget filterDialog(BuildContext context) {
    return AlertDialog(
      actionsPadding: EdgeInsets.all(2),
      title: Text('Car Filters'),
      content: new Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Text("Fuel"),
                Expanded(
                  child: Container(
                    color: Colors.white,
                  ),
                ),
                DropDownList()
              ],
            ),
            Row(children: [Text("Brand")]),
            Row(children: [Text("Year")]),
            Row(children: [Text("Price")]),
          ]),
      actions: [
        RaisedButton(
          onPressed: () {
            Navigator.of(context).pop();
          },
          color: Colors.blue,
          child: Text('Search'),
        ),
      ],
    );
  }

  void goToCar(BuildContext context, Car car) {
    Navigator.of(context).push(MaterialPageRoute<void>(
      builder: (BuildContext context) {
        return CarView(car: car);
      },
    ));
  }

  @override
  void initState() {
    super.initState();
    fuelDropDown = buildDropDown(fuelFilterItems);
    fuelSelected = fuelFilterItems[0];
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
                          title: Text(car.brand + " ${car.model}",
                              style: Theme.of(context).textTheme.bodyText1),
                          subtitle: Text(
                              "X meters | ${car.price_per_minute} €/m",
                              style: Theme.of(context).textTheme.bodyText2),
                          onTap: () {
                            goToCar(context, car);
                          },
                        ),
                      )
                      .toList(),
                );
              } else {
                return Center(child: CircularProgressIndicator());
              }
            }),
        floatingActionButton: FloatingActionButton(
          onPressed: () {
            showDialog(
                context: context,
                builder: (BuildContext context) => filterDialog(context));
          },
          child: Icon(Icons.filter_list),
        ));
  }
}
