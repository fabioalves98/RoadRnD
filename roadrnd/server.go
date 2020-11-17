package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	_ "reflect"

	"github.com/gin-gonic/gin"
)

type Car struct {
	Brand            string
	FuelType         string
	Id               string
	Kms              int
	Model            string
	Num_of_seats     int
	Owner            string
	Photo            string
	RegistrationYear string
}

type CarLocation struct {
	Car_id   string
	Location string
	Status   string
}

func main() {
	r := gin.Default()
	r.GET("/cars", func(c *gin.Context) {

		// Get Car location from Car Location
		resp, err := http.Get("http://172.18.0.1:5002/car")
		if err != nil {
			log.Fatalln(err)
		}
		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatalln(err)
		}

		// Convert to CarLocation Structure
		var loc []CarLocation
		json.Unmarshal([]byte(body), &loc)
		if err != nil {
			log.Println("Error Parsing Location JSON data - ", err)
		}

		pretty_loc, err := json.MarshalIndent(loc, "", "    ")
		log.Println(string(pretty_loc))

		// Get Cars from Car Inventory
		resp, err = http.Get("http://172.18.0.1:5001/car")
		if err != nil {
			log.Fatalln(err)
		}
		body, err = ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatalln(err)
		}

		// Convert to Car Structure
		var cars []Car
		err = json.Unmarshal([]byte(body), &cars)

		if err != nil {
			log.Println("Error Parsing Inventory JSON data - ", err)
		}

		pretty_inv, err := json.MarshalIndent(cars, "", "    ")
		log.Println(string(pretty_inv))

		c.JSON(200, cars)
	})

	r.Run() // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
}
