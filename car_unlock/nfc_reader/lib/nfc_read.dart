import 'dart:async';
import 'dart:io' show Platform;
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter/services.dart';
import 'package:flutter_nfc_kit/flutter_nfc_kit.dart';

class NFCRead {
  final String host;
  NFCRead(this.host);

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

  Future<String> unlock(String id, String tag) async {
    print("Unlock");
    final response = await http.post(host + '/unlock',
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{'id': id, 'tag': tag}));

    if (response.statusCode == 200) {
      return response.body;
    } else {
      print(response.statusCode);
      return "Error";
    }
  }

  Future<String> lock(String id, String tag) async {
    print("Lock");
    final response = await http.post(host + '/lock',
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{'id': id, 'tag': tag}));

    if (response.statusCode == 200) {
      return response.body;
    } else {
      print(response.statusCode);
      return "Error";
    }
  }

  Future<String> add(String id, String tag) async {
    print("Add");
    final response = await http.post(host + '/add',
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{'id': id, 'tag': tag}));

    if (response.statusCode == 200) {
      return response.body;
    } else {
      print(response.statusCode);
      return "Error";
    }
  }

  Future<String> delete(String id) async {
    print("Delete");
    final response = await http.post(host + '/delete',
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{'id': id}));

    if (response.statusCode == 200) {
      return response.body;
    } else {
      print(response.statusCode);
      return "Error";
    }
  }

  Future<String> updateTag(String id, String tag) async {
    print("Update tag");
    final response = await http.post(host + '/updateTag',
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{'id': id, 'tag': tag}));

    if (response.statusCode == 200) {
      return response.body;
    } else {
      print(response.statusCode);
      return "Error";
    }
  }
}
