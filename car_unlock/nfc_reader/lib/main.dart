import 'package:flutter/material.dart';
import 'nfc_read.dart';

void main() => runApp(MaterialApp(home: MainApp()));

class MainApp extends StatefulWidget {
  @override
  _MainAppState createState() => _MainAppState();
}

class _MainAppState extends State<MainApp> with SingleTickerProviderStateMixin {
  NFCRead nfc = NFCRead("http://40.115.31.209:5003");

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
                      /* return Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: <Widget>[
                            Text(
                              'Platform: ${nfc.getPlataform()} \nTag ID: $res',
                              textAlign: TextAlign.center,
                            ),
                          ],
                        ),
                      ); */
                      return FutureBuilder(
                          /* Dummy unlock test */
                          future: nfc.unlock("AA-01-AA", "tag1"),
                          builder: (BuildContext context,
                              AsyncSnapshot<String> snapshot) {
                            if (snapshot.hasData) {
                              res = snapshot.data;
                              return Center(
                                child: Column(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: <Widget>[
                                    /* Should appear response body from service */
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
                                    Text('Cenas'),
                                  ],
                                ),
                              );
                            }
                          });
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
