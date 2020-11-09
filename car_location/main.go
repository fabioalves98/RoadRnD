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
	fmt.Printf("TESTING DB\n")
	

	// Test db

	// _, err = db.Exec("INSERT INTO Cars (car_id, location, status) VALUES ('1342513', '40.3213, 32.3213', 'Rented');")

	if err != nil {
		panic(err)
	}
	
	rows, err := db.Query("SELECT car_id, location, status FROM Cars")
	if err != nil {
		// handle this error better than this
		panic(err)
	}
	defer rows.Close()
	
	for rows.Next() {
		var id string
		var location string
		var status string
		err = rows.Scan(&id, &location, &status)
		if err != nil {
		  // handle this error
		  panic(err)
		}
		fmt.Println(id, location, status)
	  }
	


	
	
	r := gin.Default()
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "pong",
		})
    })


    // Creating all routes

    r.POST("/update_status", updateVehicleStatus)
    r.GET("/car_location", getCarLocation)
	r.POST("/car_location", addNewCarLocation)

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


func updateVehicleStatus(c *gin.Context){

    c.JSON(200, gin.H{
        "message": "status_page",
    })
}

func getCarLocation(c *gin.Context){

	// Should parse params like the location asked, the status of cars
	// asked (currently rented, not yet rented)....
	car_locations := []car{}
	example1 := car{Car_id: "7837289", Location: "41.40338, 2.17403", Status: "Rented"}
	example2 := car{Car_id: "4782917", Location: "44.23331, 7.63727", Status: "Rented"}
	car_locations = append(car_locations, example1)
	car_locations = append(car_locations, example2)

	c.JSON(200, gin.H{
		"code" : 200,
		// Returns array of corresponding cars using {carid: DecimalDegrees}
		"message" : car_locations,
	})

}

func addNewCarLocation(c *gin.Context){

	var car car;
	c.BindJSON(&car)

	// Add this car to the DB

	c.JSON(200, gin.H{"status": car.Status}) // Your custom response here

}