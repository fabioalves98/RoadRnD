package database

import ("fmt"
"database/sql"
_"github.com/lib/pq"
"../common";
)

const (
	host     = "postgres"
	port     = 5432
	user     = "db"
	password = "db_pass"
	dbname   = "db"
)
  

var DB = getDBContext()

func getDBContext() (db *sql.DB){
	conn_string := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable", host, port, user, password, dbname)
	db, err := sql.Open("postgres", conn_string)



	if err != nil {
		panic(err)
	}

	return db
}

func InitDB(){
	
	// Check if the db exists. if it doesnt, create it and insert a couple of values
	statement := `SELECT EXISTS(SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('CarLocationDB'));`
	row := DB.QueryRow(statement)
	var exists bool
	row.Scan(&exists)

	if exists == false {
		DB.Exec("CREATE DATABASE CarLocationDB")

		fmt.Printf("Created to database 'CarLocationDB'!\n")

		DB.Exec("CREATE TABLE CarLocation (car_id varchar(16) PRIMARY KEY, location varchar(255), status varchar(255))")
		
		fmt.Printf("Created table 'CarLocation'\n")

		_, _ = DB.Exec("INSERT INTO CarLocation (car_id, location, status) VALUES ('AA-01-AA', '40.3213, 32.3213', 'Rented');")
		_, _ = DB.Exec("INSERT INTO CarLocation (car_id, location, status) VALUES ('GD-02-XA', '40.3421, 31.3232', 'Rented');")
		_, _ = DB.Exec("INSERT INTO CarLocation (car_id, location, status) VALUES ('LD-34-CV', '39.8432, 31.7403', 'Parked');")
		_, _ = DB.Exec("INSERT INTO CarLocation (car_id, location, status) VALUES ('RT-10-SA', '41.3214, 32.6313', 'Parked');")
		
		TestDB()
	}

	fmt.Printf("Database exists and is ready to run!!\n")
	
}

func TestDB(){
	rows, err := DB.Query("SELECT car_id, location, status FROM CarLocation")

	if err != nil {
		panic(err)
	}

	fmt.Printf("Current values in database\n")

	for rows.Next() {
		var id string
		var location string
		var status string
		rows.Scan(&id, &location, &status)
		fmt.Println(id, location, status)
	}

}

func InsertCarLocation(car_id, location, status string) bool{

	_, err := DB.Exec("INSERT INTO CarLocation (car_id, location, status) VALUES ($1, $2, $3);", car_id, location, status)
	
	if err != nil {
		fmt.Printf("> Error inserting in the database!\n")
		fmt.Println(err.Error())
		return false
	}

	TestDB()

	return true

}

func SelectCar(car_id string) common.CarLocation{

	row := DB.QueryRow("SELECT car_id, location, status FROM CarLocation WHERE car_id=$1", car_id)
	
	
	var id string
	var location string
	var status string
	err := row.Scan(&id, &location, &status);

	if err != nil {
		fmt.Printf("> Error fetching from the database!\n")
		fmt.Println(err.Error())
	}

	var car = common.CarLocation{Car_id: id, Location: location, Status: status};

	return car

}

func SelectAll() []common.CarLocation{
	car_locations := []common.CarLocation{}

	rows, err := DB.Query("SELECT car_id, location, status FROM CarLocation")

	if err != nil {
		fmt.Printf("> Error fetching from the database!\n")
		fmt.Println(err.Error())	
	}

	fmt.Printf("Current values in database\n")

	for rows.Next() {
		var id string
		var location string
		var status string
		rows.Scan(&id, &location, &status)
		var car = common.CarLocation{Car_id: id, Location: location, Status: status}
		car_locations = append(car_locations, car)
	}
	return car_locations
}

func UpdateCar(car_id, location, status string) bool{

	if location != ""{
		_, err := DB.Exec("UPDATE CarLocation SET location = $2 WHERE car_id = $1;", car_id, location)
		common.Check(err, "Can't update database\n")
	}else if status != ""{
		_, err := DB.Exec("UPDATE CarLocation SET status = $2 WHERE car_id = $1;", car_id, status)
		common.Check(err, "Can't update database\n")
	}else{
		_, err := DB.Exec("UPDATE CarLocation SET location = $3, status = $2 WHERE car_id = $1;", car_id, status, location)	
		common.Check(err, "Can't update database\n")
	}



	return true
}
