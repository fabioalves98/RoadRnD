class Car {
  final String brand;
  final String model;
  final String id;
  final String fuel_type;
  final int kms;
  final int num_of_seats;
  final String owner;
  final int price_per_minute;
  final String year;

  Car(
      {this.brand,
      this.model,
      this.id,
      this.fuel_type,
      this.kms,
      this.num_of_seats,
      this.owner,
      this.price_per_minute,
      this.year});

  factory Car.fromJson(Map<String, dynamic> json) {
    return Car(
        brand: json['Brand'],
        model: json['Model'],
        id: json['Id'],
        fuel_type: json['FuelType'],
        kms: json['Kms'],
        num_of_seats: json['Num_of_seats'],
        owner: json['Owner'],
        price_per_minute: json['Price_per_minute'],
        year: json['RegistrationYear']);
  }
}
