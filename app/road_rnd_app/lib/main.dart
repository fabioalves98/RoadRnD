import 'package:flutter/material.dart';

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
      itemCount: _cars.length,
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
      body: _buildSuggestions(),
    );
  }
}
