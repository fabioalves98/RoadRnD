import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_inappwebview/flutter_inappwebview.dart';
import 'dart:async';
import 'dart:convert';

import 'global.dart';
import 'car.dart';

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
      );
    }));
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

  Column priceCounter() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text(
          "Price Counter",
          style: Theme.of(context).textTheme.bodyText1,
        ),
        Text(
          (locked && !used) ? "" : "$curPrice €",
          style: Theme.of(context).textTheme.bodyText1,
        )
      ],
    );
  }

  void lockUnlock() {
    if (locked) {
      print('Unlock Car - ${widget.car.id}');
      startCount();
    } else {
      print('Lock Car - ${widget.car.id}');
      stopCount();
    }
    setState(() {
      locked = !locked;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text('${widget.car.brand} ${widget.car.model}'),
        ),
        body: Container(
            padding: const EdgeInsets.all(32),
            child: Column(
              children: [
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
                      infoEntry("Price", "${widget.car.price_per_minute}")
                    ])),
                Expanded(child: priceCounter()),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    RaisedButton(
                        textColor: Colors.black,
                        onPressed: (locked && used) ? null : lockUnlock,
                        child: Text(
                          locked ? "Unlock" : "Lock",
                          style: Theme.of(context).textTheme.bodyText1,
                        )),
                    RaisedButton(
                        textColor: Colors.black,
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
