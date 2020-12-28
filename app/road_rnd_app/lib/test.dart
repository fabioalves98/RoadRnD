import 'package:flutter/material.dart';

class Test extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        home: Scaffold(
            appBar:
                AppBar(title: Text('Change Text Dynamically on Button Click')),
            body: Center(child: UpdateText())));
  }
}

class UpdateText extends StatefulWidget {
  UpdateTextState createState() => UpdateTextState();
}

class UpdateTextState extends State {
  bool textChange = true;

  changeText() {
    setState(() {
      textChange = !textChange;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Center(
            child: Column(children: <Widget>[
      Container(
          padding: EdgeInsets.fromLTRB(20, 20, 20, 20),
          child: Text(textChange ? "First" : "Second",
              style: TextStyle(fontSize: 21))),
      RaisedButton(
        onPressed: () => changeText(),
        child: Text('Click Here To Change Text Widget Text Dynamically'),
        textColor: Colors.white,
        color: Colors.green,
        padding: EdgeInsets.fromLTRB(10, 10, 10, 10),
      ),
    ])));
  }
}
