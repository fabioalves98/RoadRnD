import 'package:flutter/material.dart';
import 'package:flutter_nfc_kit/flutter_nfc_kit.dart';
import 'nfc_read.dart';

void main() => runApp(MaterialApp(home: MainApp()));

class MainApp extends StatefulWidget {
  @override
  _MainAppState createState() => _MainAppState();
}

class _MainAppState extends State<MainApp> with SingleTickerProviderStateMixin {
  NFCRead nfc = NFCRead();

  @override
  Widget build(BuildContext context) {
    String res;
    return Scaffold(
      appBar: AppBar(title: Text('RoadRnD')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            FutureBuilder(
                future: nfc.readTag(),
                builder:
                    (BuildContext context, AsyncSnapshot<String> snapshot) {
                  print(snapshot.data);
                  if (snapshot.hasData) {
                    if (snapshot.data != "NFC Not Available" &&
                        snapshot.data != "Reading NFC Tag") {
                      res = snapshot.data;
                      return Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: <Widget>[
                            Text(
                              'Platform: ${nfc.getPlataform()} \nTag ID: $res',
                              textAlign: TextAlign.center,
                            ),
                          ],
                        ),
                      );
                    } else {
                      return Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: <Widget>[
                            Text('${snapshot.data}'),
                          ],
                        ),
                      );
                    }
                  } else {
                    return Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: <Widget>[
                          Text('Reading NFC Tag on ${nfc.getPlataform()}'),
                        ],
                      ),
                    );
                  }
                }),
          ],
        ),
      ),
    );
  }
}
