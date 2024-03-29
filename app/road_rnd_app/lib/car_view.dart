import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_inappwebview/flutter_inappwebview.dart';
import 'dart:async';
import 'dart:convert';

import 'global.dart';
import 'car.dart';
import 'nfc_read.dart';

class CarView extends StatefulWidget {
  final Car car;

  const CarView({Key key, this.car}) : super(key: key);

  @override
  CarViewState createState() => CarViewState();
}

class CarViewState extends State<CarView> {
  bool locked = true;
  bool used = false;
  int seconds = 0;
  double curPrice = 0;
  Timer timer;
  NFCRead nfc = NFCRead("http://roadrnd.westeurope.cloudapp.azure.com:5003");

  void startCount() {
    timer = Timer.periodic(
        Duration(milliseconds: 1000), (Timer t) => updatePrice());
    setState(() {
      used = true;
    });
  }

  void stopCount() {
    timer.cancel();
    seconds = 0;
  }

  void updatePrice() {
    seconds++;
    setState(() {
      curPrice = seconds * widget.car.price_per_minute / 100;
    });
  }

  void goToPay(BuildContext context) async {
    print("Executing Payment");

    final response = await http.post(
      Global.lt_link + '/create_payment',
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        "Authorization": Global.token
      },
      body: jsonEncode(
          <String, String>{'CarID': widget.car.id, 'Price': "$curPrice"}),
    );

    print(response.body);

    String paymentID = response.body;

    Navigator.of(context)
        .push(MaterialPageRoute<void>(builder: (BuildContext context) {
      return InAppWebView(
        initialUrl:
            'http://roadrnd.westeurope.cloudapp.azure.com:5006/approve/$paymentID',
        onLoadStart: (InAppWebViewController controller, String url) {
          print(url);
          if (url ==
              'http://roadrnd.westeurope.cloudapp.azure.com:5006/finish/$paymentID') {
            Navigator.pop(context);
            setState(() {
              locked = true;
              used = false;
              curPrice = 0;
            });
          }
        },
      );
    }));
  }

  Container carTitle(String title) {
    return Container(
      child: Row(
        children: [
          Text(
            title,
            style: Theme.of(context).textTheme.headline3,
          ),
        ],
      ),
      margin: const EdgeInsets.only(bottom: 20.0),
    );
  }

  Container carImage(String image) {
    return Container(
        width: 300.0,
        color: Colors.yellow,
        child: Image.network(
          "${widget.car.photo}",
          fit: BoxFit.fitWidth,
        ));
  }

  Row infoEntry(String label, String value) {
    return Row(children: [
      Text(label, style: Theme.of(context).textTheme.bodyText1),
      Expanded(
        child: Container(
          color: Colors.white,
        ),
      ),
      Text(value, style: Theme.of(context).textTheme.bodyText2)
    ]);
  }

  Container priceCounter() {
    return Container(
      margin: const EdgeInsets.only(bottom: 50.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(
            "Price Counter",
            style: Theme.of(context).textTheme.bodyText1,
          ),
          Text(
            (locked && !used) ? "" : "$curPrice €",
            style: Theme.of(context).textTheme.bodyText2,
          )
        ],
      ),
    );
  }

  Widget unlockDialog(BuildContext context) {
    return AlertDialog(
      title: Text('Car Unlock'),
      content: new Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [Text("Use NFC to Unlock the car")]),
      actions: [
        FlatButton(
          onPressed: () {
            Navigator.of(context).pop();
          },
          textColor: Theme.of(context).primaryColor,
          child: Text('Close'),
        ),
      ],
    );
  }

  void unlockCar() async {
    print('Unlock Car - ${widget.car.id}');

    String nfc_result = await nfc.readTag();
    print(nfc_result);

    if (nfc_result == "NFC Not Available") {
      String unlock_result =
          await nfc.unlock(widget.car.id, "tag1", Global.token);
      print(unlock_result);
    }
  }

  void lockCar() async {
    print('Lock Car - ${widget.car.id}');

    String nfc_result = await nfc.readTag();
    print(nfc_result);

    if (nfc_result == "NFC Not Available") {
      String lock_result = await nfc.lock(widget.car.id, "tag1", Global.token);
      print(lock_result);
    }
  }

  void lockUnlock() async {
    if (locked) {
      await showDialog(
              context: context,
              builder: (BuildContext context) => unlockDialog(context))
          .then((value) {
        unlockCar();
        startCount();
      });
    } else {
      stopCount();
      lockCar();
    }
    setState(() {
      locked = !locked;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text('Rent a Car'),
        ),
        body: Container(
            padding: EdgeInsets.all(32),
            child: Column(
              children: [
                carTitle("${widget.car.brand} ${widget.car.model}"),
                carImage("${widget.car.photo}"),
                // Image.network("${widget.car.photo}"),
                Expanded(
                    child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                      infoEntry("ID", "${widget.car.id}"),
                      infoEntry("Fuel", "${widget.car.fuel_type}"),
                      infoEntry("Kms", "${widget.car.kms}"),
                      infoEntry("Seats", "${widget.car.num_of_seats}"),
                      infoEntry("Year", "${widget.car.year}"),
                      infoEntry("Owner", "${widget.car.owner}"),
                      infoEntry(
                          "Price", "${widget.car.price_per_minute / 100} €/m")
                    ])),
                priceCounter(),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    RaisedButton(
                        color: Colors.blue,
                        onPressed: (locked && used) ? null : lockUnlock,
                        child: Text(
                          locked ? "Unlock" : "Lock",
                          style: Theme.of(context).textTheme.bodyText1,
                        )),
                    RaisedButton(
                        color: Colors.blue,
                        onPressed:
                            (locked && used) ? () => goToPay(context) : null,
                        child: Text(
                          "Pay",
                          style: Theme.of(context).textTheme.bodyText1,
                        ))
                  ],
                ),
              ],
            )));
  }
}
