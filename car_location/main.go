package main

import ("fmt"
"github.com/gin-gonic/gin"
"./database";
"./common";
)



func main() {

	// database.DB.Exec("DROP TABLE CarLocation")
	// database.DB.Exec("DROP DATABASE CarLocationDB")
	database.InitDB()

	fmt.Printf("Current values in database FROM MAIN\n")
	
	// database.ClearDB()
	// database.InsertDummyDB()
	database.TestDB()

	// TODO: Add search by location. Add Delete methods

	r := gin.Default()
    // Creating all routes
	r.GET("/car", getCarInformation)
	r.POST("/car/:car_id", insertNewCar)

	r.GET("/car_location/:car_id", getCarLocation)
	r.PUT("/car_location/:car_id", updateCarLocation)

	r.GET("/car_status/:car_id", getCarStatus)
	r.PUT("/car_status/:car_id", updateCarStatus)


	r.Run() // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
}


func getCarInformation(c *gin.Context){
	
	var loc = common.Location{}
	c.BindJSON(&loc)
	car_locations := []common.CarLocation{}
	// if loc.Coords != ""
	if loc.Coords == ""{
		car_locations = database.SelectAll()
	}else{
		car_locations = database.SelectFromLocation(loc.Coords, loc.Radius)
		if len(car_locations) == 0 {
			c.JSON(200, "No cars around the provided location. Try increasing search radius!")
			return
		}
	}


	c.JSON(200, car_locations)

}

func insertNewCar(c *gin.Context){

	var car = common.CarLocation{Car_id: c.Param("car_id")};
	c.BindJSON(&car) // This parses the body param json into car
	
	success := database.InsertCarLocation(car.Car_id, car.Location, car.Status)

	if success{
		c.JSON(200, gin.H{"AddedCar": car}) // temporary for checking information
	}else{
		c.JSON(500, gin.H{"Error": "An error occured! (e.g. Database duplicate keys...)"})
	}
}

func getCarLocation(c *gin.Context){

	id := c.Param("car_id")
	// example1 := CarLocation{Car_id: id, Location: "41.40338, 2.17403", Status: "Rented"}

	// Fetch specific car from DB
	var car = database.SelectCar(id)
	
	
	c.JSON(200, gin.H{"code": 200, "message": car.Location})

}

func updateCarLocation(c *gin.Context){
	
	var car = common.CarLocation{Car_id: c.Param("car_id")};
	c.BindJSON(&car)
	// id := c.Param("car_id") // This adds the missing ID


	// Update specific entrance "id" with information in "car"
	database.UpdateCar(car.Car_id, car.Location, "")


	c.JSON(200, "OK") // temporary for checking information

}


func getCarStatus(c *gin.Context){

	id := c.Param("car_id")
	// example1 := common.CarLocation{Car_id: id, Location: "41.40338, 2.17403", Status: "Parked"}

	// Fetch specific car from DB
	var car = database.SelectCar(id)

	
	c.JSON(200, gin.H{"code": 200, "message": car.Status})

}

func updateCarStatus(c *gin.Context){
	
	var car = common.CarLocation{Car_id: c.Param("car_id")};
	c.BindJSON(&car)
	// id := c.Param("car_id") // This adds the missing ID


	// Update specific entrance "id" with location in "car"
	database.UpdateCar(car.Car_id, "", car.Status)

	c.JSON(200, "OK") // temporary for checking information

}




