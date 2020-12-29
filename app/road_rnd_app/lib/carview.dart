import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_inappwebview/flutter_inappwebview.dart';
import 'dart:async';

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
  int seconds = 0;
  Timer timer;

  void startCount() {
    timer = Timer.periodic(
        Duration(milliseconds: 1000), (Timer t) => updatePrice());
  }

  void stopCount() {
    timer.cancel();
    int price = seconds * widget.car.price_per_minute;
    seconds = 0;
    print("Preço Final - $price");
  }

  void updatePrice() {
    seconds++;
    print(seconds);
  }

  void goToPay(BuildContext context) async {
    print("Executing Payment");

    final response = await http.get(Global.lt_link + '/create_payment');

    print(response.body);

    String payment_id = response.body;

    Navigator.of(context)
        .push(MaterialPageRoute<void>(builder: (BuildContext context) {
      return InAppWebView(
        initialUrl:
            'http://roadrnd.westeurope.cloudapp.azure.com:5006/approve/$payment_id',
      );
    }));
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
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                      Text(
                        "ID - ${widget.car.id}",
                        style: Theme.of(context).textTheme.bodyText1,
                      ),
                      Text(
                        "Fuel - ${widget.car.fuel_type}",
                        style: Theme.of(context).textTheme.bodyText1,
                      ),
                      Text(
                        "Kms - ${widget.car.kms}",
                        style: Theme.of(context).textTheme.bodyText1,
                      ),
                      Text(
                        "Seats - ${widget.car.num_of_seats}",
                        style: Theme.of(context).textTheme.bodyText1,
                      ),
                      Text(
                        "Year - ${widget.car.year}",
                        style: Theme.of(context).textTheme.bodyText1,
                      ),
                      Text(
                        "Owner - ${widget.car.owner}",
                        style: Theme.of(context).textTheme.bodyText1,
                      ),
                      Text(
                        "Price - ${widget.car.price_per_minute}",
                        style: Theme.of(context).textTheme.bodyText1,
                      )
                    ])),
                OutlineButton(
                    textColor: Color(0xFF6200EE),
                    highlightedBorderColor: Colors.black.withOpacity(0.12),
                    onPressed: () {
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
                    },
                    child: Text(
                      locked ? "Unlock" : "Lock",
                      style: Theme.of(context).textTheme.bodyText1,
                    )),
                OutlineButton(
                    textColor: Color(0xFF6200EE),
                    highlightedBorderColor: Colors.black.withOpacity(0.12),
                    onPressed: () {
                      print('Pay Car Rent - ${widget.car.id}');
                      goToPay(context);
                    },
                    child: Text(
                      "Pay",
                      style: Theme.of(context).textTheme.bodyText1,
                    ))
              ],
            )));
  }
}
