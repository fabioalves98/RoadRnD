package database

import ("fmt"
"strings"
"strconv"
"database/sql"
_"github.com/lib/pq"
"github.com/cridenour/go-postgis"
	// "github.com/paulmach/orb/encoding/wkb"
"../common";
)

const (
	host     = "postgres"
	port     = 5432
	user     = "db"
	password = "db_pass"
	dbname   = "db"
)

type AuxPoint struct {
	Point postgis.PointS
}

func (p *AuxPoint) Scan(src interface{}) error {
	switch val := src.(type) {
	case []byte:
		return p.Point.Scan(val)
	case string:
		return p.Point.Scan([]byte(val))
	}
	return nil
	//return error.New("AuxPoint: unsupported type")
}

 

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
	DB.Exec("CREATE EXTENSION IF NOT EXISTS postgis")

	if exists == false {
		DB.Exec("CREATE DATABASE CarLocationDB")

		fmt.Printf("Created to database 'CarLocationDB'!\n")

		DB.Exec("CREATE TABLE CarLocation (car_id varchar(16) PRIMARY KEY, location varchar(255), status varchar(255))")
		
		fmt.Printf("Created table 'CarLocation'\n")

		InsertDummyDB()
		TestDB()
	}

	fmt.Printf("Database exists and is ready to run!!\n")
	
}

func InsertDummyDB(){
	
	point := postgis.PointS{4326, 40.3213, 32.3213}
	
	_, _ = DB.Exec("INSERT INTO CarLocation (car_id, location, status) VALUES ('AA-01-AA', GeomFromEWKB($1), 'Rented');", point)
	point = postgis.PointS{4326, 40.3421, 31.3232}
	_, _ = DB.Exec("INSERT INTO CarLocation (car_id, location, status) VALUES ('GD-02-XA', GeomFromEWKB($1), 'Rented');", point)
	point = postgis.PointS{4326, 40.3421, 31.3253}
	_, _ = DB.Exec("INSERT INTO CarLocation (car_id, location, status) VALUES ('LD-34-CV', GeomFromEWKB($1), 'Parked');", point)
	point = postgis.PointS{4326, 40.3256, 31.3275}	
	_, _ = DB.Exec("INSERT INTO CarLocation (car_id, location, status) VALUES ('RT-10-SA', GeomFromEWKB($1), 'Parked');", point)

}

func ClearDB(){

	statement := `DELETE FROM CarLocation`
	_, err := DB.Exec(statement)
	common.Check(err, "Error clearing database")
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

	point := locationStringToPoint(location)
	_, err := DB.Exec("INSERT INTO CarLocation (car_id, location, status) VALUES ($1, GeomFromEWKB($2), $3);", car_id, point, status)

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
	var location AuxPoint
	var status string
	err := row.Scan(&id, &location, &status);

	if err != nil {
		fmt.Printf("> Error fetching from the database!\n")
		fmt.Println(err.Error())
	}

	var car = common.CarLocation{Car_id: id, Location: pointToLocationString(location.Point), Status: status};

	return car

}


func SelectAll() []common.CarLocation{
	car_locations := []common.CarLocation{}

	rows, err := DB.Query("SELECT car_id, location, status FROM CarLocation")
	// rows, err := DB.Query("SELECT location FROM CarLocation")

	if err != nil {
		fmt.Printf("> Error fetching from the database!\n")
		fmt.Println(err.Error())	
	}

	fmt.Printf("Current values in database\n")


	for rows.Next() {
		var id string
		var location_p AuxPoint
		var status string

		
		rows.Scan(&id, &location_p, &status)
		fmt.Println(location_p)
		var car = common.CarLocation{Car_id: id, Location: pointToLocationString(location_p.Point), Status: status}
		car_locations = append(car_locations, car)
	}
	return car_locations
}

func SelectFromLocation(location string, radius float32) []common.CarLocation{
	point := locationStringToPoint(location)
	car_locations := []common.CarLocation{}
	statement := "SELECT * FROM CarLocation WHERE ST_DWithin(location, GeomFromEWKB($1), $2);"
	rows, err := DB.Query(statement, point, radius)

	common.Check(err, "Couldn't fetch from database");

	for rows.Next() {
		var id string
		var location_p AuxPoint
		var status string

		
		rows.Scan(&id, &location_p, &status)
		fmt.Println(location_p)
		var car = common.CarLocation{Car_id: id, Location: pointToLocationString(location_p.Point), Status: status}
		car_locations = append(car_locations, car)
	}
	return car_locations

}

func UpdateCar(car_id, location, status string) bool{

	if location != ""{
		point := locationStringToPoint(location)
		_, err := DB.Exec("UPDATE CarLocation SET location = GeomFromEWKB($2) WHERE car_id = $1;", car_id, point)
		common.Check(err, "Can't update database\n")
	}else if status != ""{
		_, err := DB.Exec("UPDATE CarLocation SET status = $2 WHERE car_id = $1;", car_id, status)
		common.Check(err, "Can't update database\n")
	}else{
		point := locationStringToPoint(location)
		_, err := DB.Exec("UPDATE CarLocation SET location = GeomFromEWKB($3), status = $2 WHERE car_id = $1;", car_id, status, point)	
		common.Check(err, "Can't update database\n")
	}



	return true
}


func locationStringToPoint(location string) (p postgis.PointS){
	// point = postgis.PointS{4326, 40.3256, 31.3275}	
	splitted := strings.Split(location, ", ")
	x, _ := strconv.ParseFloat(splitted[0], 64)
	y, _ := strconv.ParseFloat(splitted[1], 64) 
	
	return postgis.PointS{4326, x, y}
}

func pointToLocationString(p postgis.PointS) (string){

	return fmt.Sprintf("%f, %f", p.X, p.Y)

}