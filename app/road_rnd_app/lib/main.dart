import 'package:flutter/material.dart';
import 'package:road_rnd_app/tabs_view.dart';

import 'login.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'RoadRnD',
      home: Login(),
    );
  }
}
