import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:road_rnd_app/car.dart';
import 'dart:convert';

import 'global.dart';
import 'car_location.dart';

class MapSample extends StatefulWidget {
  @override
  _MapSampleState createState() => _MapSampleState();
}

class _MapSampleState extends State<MapSample> {
  GoogleMapController mapController;

  final LatLng _center = const LatLng(40.640786, -8.654378);
  final Map<String, Marker> markers = {};
  BitmapDescriptor pinLocationIcon;

  Future<void> _onMapCreated(GoogleMapController controller) async {
    mapController = controller;

    final response = await http.get(Global.lt_link + '/map');

    print(response.body);

    if (response.statusCode == 200) {
      final json = jsonDecode(response.body);

      var car_location_list = new List<CarLocation>();
      if (json != null) {
        json.forEach((element) {
          final car_location = CarLocation.fromJson(element);
          car_location_list.add(car_location);
        });

        print(car_location_list.length);

        setState(() {
          markers.clear();
          for (CarLocation loc in car_location_list) {
            double lat = double.parse(loc.location.split(', ')[0]);
            double long = double.parse(loc.location.split(', ')[1]);

            final marker = Marker(
                markerId: MarkerId(loc.id),
                position: LatLng(lat, long),
                infoWindow: InfoWindow(title: loc.id),
                icon: pinLocationIcon);
            markers[loc.id] = marker;
          }
        });
      }
    } else {
      // If the server did not return a 200 OK response,
      // then throw an exception.
      throw Exception('Failed to load album');
    }
  }

  void setCustomMapPin() async {
    pinLocationIcon = await BitmapDescriptor.fromAssetImage(
        ImageConfiguration(devicePixelRatio: 1), 'assets/car.png');
  }

  @override
  void initState() {
    super.initState();
    setCustomMapPin();
  }

  @override
  Widget build(BuildContext context) {
    return GoogleMap(
      onMapCreated: _onMapCreated,
      initialCameraPosition: CameraPosition(
        target: _center,
        zoom: 15.0,
      ),
      markers: markers.values.toSet(),
    );
  }
}
