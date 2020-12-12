import 'dart:async';
import 'dart:io' show Platform;
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter/services.dart';
import 'package:flutter_nfc_kit/flutter_nfc_kit.dart';

class NFCRead {
  String getPlataform() {
    return '${Platform.operatingSystem} ${Platform.operatingSystemVersion}';
  }

  Future<NFCAvailability> isAvailable() async {
    NFCAvailability availability;
    try {
      availability = await FlutterNfcKit.nfcAvailability;
    } on PlatformException {
      availability = NFCAvailability.not_supported;
    }

    return availability;
  }

  Future<String> readTag() async {
    NFCAvailability availability = await FlutterNfcKit.nfcAvailability;
    if (availability != NFCAvailability.available) {
      return "NFC Not Available";
    }

    print("Reading NFC tag");
    NFCTag tag;
    String result;
    try {
      tag = await FlutterNfcKit.poll();

      if (tag.standard == "ISO 14443-4 (Type B)") {
        String result1 = await FlutterNfcKit.transceive("00B0950000");
        String result2 =
            await FlutterNfcKit.transceive("00A4040009A00000000386980701");
        result = '1: $result1\n2: $result2\n';
      } else if (tag.type == NFCTagType.iso18092) {
        String result1 = await FlutterNfcKit.transceive("060080080100");
        result = '1: $result1\n';
      } else if (tag.type == NFCTagType.mifare_ultralight ||
          tag.type == NFCTagType.mifare_classic) {
        var ndefRecords = await FlutterNfcKit.readNDEFRecords();
        var ndefString = ndefRecords
            .map((r) => r.toString())
            .reduce((value, element) => value + "\n" + element);
        result = '1: $ndefString\n';
      }
    } catch (e) {
      result = 'error: $e';
    }
    if (tag != null) {
      print("Tag ID: ${tag.id} \n Result: $result");
      return tag.id;
    } else {
      return "Reading NFC Tag";
    }
  }

  Future<String> unlockCar(String license, String tag) async {
    print("Unlock car");
    final response = await http.post('http://40.115.31.209:5003/unlock',
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{'id': license, 'tag': tag}));

    if (response.statusCode == 200) {
      print(response.body);
      return "Car Unlocked";
    } else {
      print(response.statusCode);
      return "Error";
    }
  }

  Future<String> lockCar(String license, String tag) async {
    print("Lock Car");
    final response = await http.post('http://40.115.31.209:5003/lock',
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{'id': license, 'tag': tag}));

    if (response.statusCode == 200) {
      print(response.body);
      return "Car Locked";
    } else {
      print(response.statusCode);
      return "Error";
    }
  }

  Future<String> addCar(String license, String tag) async {
    print("Add car");
    final response = await http.post('http://40.115.31.209:5003/add',
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{'id': license, 'tag': tag}));

    if (response.statusCode == 200) {
      print(response.body);
      return "Car Added";
    } else {
      print(response.statusCode);
      return "Error";
    }
  }

  Future<String> delCar(String license) async {
    print("Delete Car");
    final response = await http.post('http://40.115.31.209:5003/delete',
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{'id': license}));

    if (response.statusCode == 200) {
      print(response.body);
      return "Car Deleted";
    } else {
      print(response.statusCode);
      return "Error";
    }
  }

  Future<String> updateTag(String license, String tag) async {
    print("Update tag");
    final response = await http.post('http://40.115.31.209:5003/updateTag',
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{'id': license, 'tag': tag}));

    if (response.statusCode == 200) {
      print(response.body);
      return "Tag updated";
    } else {
      print(response.statusCode);
      return "Error";
    }
  }
}

/* class _NFCReadState extends State<NFCRead> with SingleTickerProviderStateMixin {
  String _platformVersion =
      '${Platform.operatingSystem} ${Platform.operatingSystemVersion}';
  NFCAvailability _availability = NFCAvailability.not_supported;
  NFCTag _tag;
  String _result;

  @override
  void initState() {
    super.initState();
    initPlatformState();
  }

  // Platform messages are asynchronous, so we initialize in an async method.
  Future<void> initPlatformState() async {
    NFCAvailability availability;
    try {
      availability = await FlutterNfcKit.nfcAvailability;
    } on PlatformException {
      availability = NFCAvailability.not_supported;
    }

    // If the widget was removed from the tree while the asynchronous platform
    // message was in flight, we want to discard the reply rather than calling
    // setState to update our non-existent appearance.
    if (!mounted) return;

    setState(() {
      // _platformVersion = platformVersion;
      _availability = availability;
    });
  }

  @override
  Widget build(BuildContext context) {
    List<String> res = ["", ""];
    return Scaffold(
      appBar: AppBar(title: Text('RoadRnD')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text('Running on: $_platformVersion\n $_availability'),
            FutureBuilder(
                future: readTag(),
                builder: (BuildContext context,
                    AsyncSnapshot<List<String>> snapshot) {
                  if (snapshot.hasData) {
                    res = snapshot.data;
                    return Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: <Widget>[
                          Text(
                            'ID: ${res[0]} \nTransceive Result: ${res[1]}',
                            textAlign: TextAlign.center,
                          ),
                        ],
                      ),
                    );
                    /* switch (widget.op) {
                      case "unlock":
                        {
                          return FutureBuilder(
                              future: unlockCar(widget.licensePlate),
                              builder: (BuildContext context,
                                  AsyncSnapshot<String> snapshot) {
                                if (snapshot.hasData) {
                                  return Center(
                                    child: Column(
                                      mainAxisAlignment:
                                          MainAxisAlignment.center,
                                      children: <Widget>[
                                        Text(
                                          'ID: ${res[0]} \nTransceive Result: ${res[1]} \n${snapshot.data}',
                                          textAlign: TextAlign.center,
                                        ),
                                      ],
                                    ),
                                  );
                                }
                              });
                        }
                        break;

                      case "lock":
                        {
                          return FutureBuilder(
                              future: lockCar(widget.licensePlate),
                              builder: (BuildContext context,
                                  AsyncSnapshot<String> snapshot) {
                                if (snapshot.hasData) {
                                  return Center(
                                    child: Column(
                                      mainAxisAlignment:
                                          MainAxisAlignment.center,
                                      children: <Widget>[
                                        Text(
                                          'ID: ${res[0]} \nTransceive Result: ${res[1]} \n${snapshot.data}',
                                          textAlign: TextAlign.center,
                                        ),
                                      ],
                                    ),
                                  );
                                }
                              });
                        }
                        break;

                      case "add":
                        {
                          return FutureBuilder(
                              future: addCar(widget.licensePlate),
                              builder: (BuildContext context,
                                  AsyncSnapshot<String> snapshot) {
                                if (snapshot.hasData) {
                                  return Center(
                                    child: Column(
                                      mainAxisAlignment:
                                          MainAxisAlignment.center,
                                      children: <Widget>[
                                        Text(
                                          'ID: ${res[0]} \nTransceive Result: ${res[1]} \n${snapshot.data}',
                                          textAlign: TextAlign.center,
                                        ),
                                      ],
                                    ),
                                  );
                                }
                              });
                        }
                        break;

                      case "delete":
                        {
                          return FutureBuilder(
                              future: delCar(widget.licensePlate),
                              builder: (BuildContext context,
                                  AsyncSnapshot<String> snapshot) {
                                if (snapshot.hasData) {
                                  return Center(
                                    child: Column(
                                      mainAxisAlignment:
                                          MainAxisAlignment.center,
                                      children: <Widget>[
                                        Text(
                                          'ID: ${res[0]} \nTransceive Result: ${res[1]} \n${snapshot.data}',
                                          textAlign: TextAlign.center,
                                        ),
                                      ],
                                    ),
                                  );
                                }
                              });
                        }
                        break;

                      case "update":
                        {
                          return FutureBuilder(
                              future: updateTag(widget.licensePlate),
                              builder: (BuildContext context,
                                  AsyncSnapshot<String> snapshot) {
                                if (snapshot.hasData) {
                                  return Center(
                                    child: Column(
                                      mainAxisAlignment:
                                          MainAxisAlignment.center,
                                      children: <Widget>[
                                        Text(
                                          'ID: ${res[0]} \nTransceive Result: ${res[1]} \n${snapshot.data}',
                                          textAlign: TextAlign.center,
                                        ),
                                      ],
                                    ),
                                  );
                                }
                              });
                        }
                        break;
                      default:
                        {
                          return Center(
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: <Widget>[
                                Text('Reading NFC Tag'),
                              ],
                            ),
                          );
                        }
                        break;
                    } */
                  } else {
                    return Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: <Widget>[
                          Text('Reading NFC Tag'),
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
} */
