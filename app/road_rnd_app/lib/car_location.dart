class CarLocation {
  final String id;
  final String location;
  final String status;

  CarLocation({this.id, this.location, this.status});

  factory CarLocation.fromJson(Map<String, dynamic> json) {
    return CarLocation(
        id: json['Car_id'], location: json['Location'], status: json['Status']);
  }
}
