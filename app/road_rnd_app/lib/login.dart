import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_inappwebview/flutter_inappwebview.dart';

import 'global.dart';
import 'browser.dart';

class Login extends StatefulWidget {
  final ChromeSafariBrowser browser =
      new MyChromeSafariBrowser(new MyInAppBrowser());

  @override
  LoginState createState() => LoginState();
}

class LoginState extends State<Login> {
  Future<String> loginLink;
  @override
  void initState() {
    super.initState();
    loginLink = fetchLoginLink();
    // Enable hybrid composition.
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: FutureBuilder(
            future: loginLink,
            builder: (BuildContext context, AsyncSnapshot snapshot) {
              if (snapshot.hasData) {
                String url = snapshot.data;
                widget.browser.open(url: url);
              }
              return CircularProgressIndicator();
            }),
      ),
    );
  }
}

Future<String> fetchLoginLink() async {
  final response = await http.get(Global.lt_link + '/login');

  print(response.body);

  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return response.body;
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load album');
  }
}
