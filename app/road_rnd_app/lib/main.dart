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
  void appBarMenuClick(String value) {
    print(value);
  }

  PopupMenuButton appBarMenu() {
    return PopupMenuButton<String>(
      onSelected: appBarMenuClick,
      itemBuilder: (BuildContext context) {
        return {'Settings', 'Exit'}.map((String choice) {
          return PopupMenuItem<String>(
            value: choice,
            child: Text(choice),
          );
        }).toList();
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: DefaultTabController(
        length: 2,
        child: Scaffold(
            appBar: AppBar(
              title: Text('RoadRnD'),
              actions: [appBarMenu()],
            ),
            body: TabBarView(
              physics: NeverScrollableScrollPhysics(),
              children: [
                MapSample(),
                ListCars(),
              ],
            ),
            bottomNavigationBar: TabBar(
                tabs: [
                  Tab(icon: Icon(Icons.map)),
                  Tab(icon: Icon(Icons.list)),
                ],
                labelColor: Colors.white,
                unselectedLabelColor: Colors.white,
                indicatorColor: Colors.white),
            backgroundColor: Colors.blue),
      ),
      theme: ThemeData(
          primaryColor: Colors.blue,
          textTheme: TextTheme(
              bodyText1: TextStyle(fontSize: 20.0, color: Colors.black),
              bodyText2: TextStyle(fontSize: 16.0, color: Colors.black54))),
    );
  }
}
