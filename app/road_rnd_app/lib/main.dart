import 'package:flutter/material.dart';

import 'listcars.dart';
import 'login.dart';
import 'map.dart';

import 'test.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(MyApp());
}

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
