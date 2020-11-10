package main

import ("fmt"
"database/sql"
"github.com/gin-gonic/gin"
_"github.com/lib/pq"
)

var DB *sql.DB

const (
	host     = "postgres"
	port     = 5432
	user     = "db"
	password = "db_pass"
	dbname   = "db"
  )
  


type car struct{
	Car_id 		string `json:"car_id"`
	Location 	string `json:"location"`
	Status 		string `json:"status"`
}


func main() {

	// TODO: Clear stuff out of main
	conn_string := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable", host, port, user, password, dbname)
	db, err := sql.Open("postgres", conn_string)

	if err != nil {
		panic(err)
	}
	defer db.Close()

	// Init db
	// _, err = db.Exec("CREATE DATABASE CarLocationDB")

	// if err != nil {
	// 	panic(err)
	// }
	// fmt.Printf("Created to database CarLocationDB!\n")

	// _, err = db.Exec("CREATE TABLE Cars (car_id varchar(16), location varchar(255), status varchar(255))")
	 
	// if err != nil {
	// 	panic(err)
	// }

	// fmt.Printf("Created table")
	// fmt.Printf("TESTING DB\n")
	

	// Test db

	// _, err = db.Exec("INSERT INTO Cars (car_id, location, status) VALUES ('1342513', '40.3213, 32.3213', 'Rented');")

	// if err != nil {
	// 	panic(err)
	// }
	
	// rows, err := db.Query("SELECT car_id, location, status FROM Cars")
	// if err != nil {
	// 	// handle this error better than this
	// 	panic(err)
	// }
	// defer rows.Close()
	
	// for rows.Next() {
	// 	var id string
	// 	var location string
	// 	var status string
	// 	err = rows.Scan(&id, &location, &status)
	// 	if err != nil {
	// 	  // handle this error
	// 	  panic(err)
	// 	}
	// 	fmt.Println(id, location, status)
	// }
	


	
	
	r := gin.Default()
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "pong",
		})
    })


    // Creating all routes

    // r.POST("/update_status", updateVehicleStatus)
    // r.GET("/car_location", getCarLocation)
	// r.POST("/car_location", addNewCarLocation)

	r.GET("/car", getCarInformation)
	r.POST("/car/:car_id", insertNewCar)

	r.GET("/car_location/:car_id", getCarLocation)
	r.PUT("/car_location/:car_id", updateCarLocation)

	r.GET("/car_status/:car_id", getCarStatus)
	r.PUT("/car_status/:car_id", updateCarStatus)

	// router.PUT("/somePut", putting)

	// router.POST("/somePost", posting)
	// router.DELETE("/someDelete", deleting)
	// router.PATCH("/somePatch", patching)
	// router.HEAD("/someHead", head)
	// router.OPTIONS("/someOptions", options)


	r.Run() // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
}

// func connectDB(){

// 	conn_string := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable", host, port, user, password, dbname)
// 	db, err := sql.Open("postgres", conn_string)

// 	if err != nil {
// 		panic(err)
// 	}
	
// 	DB = db
// }

// func initDB(){

// }

// func testDB(){


// }



func getCarInformation(c *gin.Context){

	// Should fetch database for all cars
	car_locations := []car{}
	example1 := car{Car_id: "AA-01-AA", Location: "41.40338, 2.17403", Status: "Rented"}
	example2 := car{Car_id: "LD-34-CV", Location: "44.23331, 7.63727", Status: "Rented"}
	car_locations = append(car_locations, example1)
	car_locations = append(car_locations, example2)

	c.JSON(200, car_locations)

}

func insertNewCar(c *gin.Context){

	var car = car{Car_id: c.Param("car_id")};
	c.BindJSON(&car) // This parses the body param json into car
	// car := c.Param("car_id") // This adds the missing ID

	// Add this car to the DB

	c.JSON(200, gin.H{"AddedCar": car}) // temporary for checking information

}

func getCarLocation(c *gin.Context){

	id := c.Param("car_id")
	example1 := car{Car_id: id, Location: "41.40338, 2.17403", Status: "Rented"}

	// Fetch specific car from DB
	
	
	c.JSON(200, gin.H{"code": 200, "message": example1.Location})

}

func updateCarLocation(c *gin.Context){
	
	var car = car{Car_id: c.Param("car_id")};
	c.BindJSON(&car)
	// id := c.Param("car_id") // This adds the missing ID


	// Update specific entrance "id" with information in "car"


	c.JSON(200, gin.H{"UpdatedCar": car}) // temporary for checking information

}


func getCarStatus(c *gin.Context){

	id := c.Param("car_id")
	example1 := car{Car_id: id, Location: "41.40338, 2.17403", Status: "Parked"}

	// Fetch specific car from DB
	
	
	c.JSON(200, gin.H{"code": 200, "message": example1.Status})

}

func updateCarStatus(c *gin.Context){
	
	var car = car{Car_id: c.Param("car_id")};
	c.BindJSON(&car)
	// id := c.Param("car_id") // This adds the missing ID


	// Update specific entrance "id" with location in "car"


	c.JSON(200, gin.H{"UpdatedCar": car}) // temporary for checking information

}




