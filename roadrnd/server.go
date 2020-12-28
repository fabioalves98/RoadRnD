package main

import (
	"bytes"
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
	Price_per_minute int
	RegistrationYear string
}

type CarLocation struct {
	Car_id   string
	Location string
	Status   string
}

func main() {
	r := gin.Default()

	r.GET("/login", func(c *gin.Context) {
		// Obtain required parameters to make request to OAuth service
		client_id := c.DefaultQuery("client_id", "123")
		redirect_url := c.DefaultQuery("redirect_url", "placeholder_url")

		log.Println(client_id)
		log.Println(redirect_url)

		// Make request to OAuth Server
		request_link := "http://roadrnd.westeurope.cloudapp.azure.com:5005/oauth/authorize?client_id=12345&redirect_url=app"

		c.String(http.StatusOK, request_link)
	})

	r.GET("/list", func(c *gin.Context) {
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
		err = json.Unmarshal([]byte(body), &loc)

		if err != nil {
			log.Println("Error Parsing Location JSON data - ", err)
		}

		pretty_loc, err := json.MarshalIndent(loc, "", "    ")
		log.Println(string(pretty_loc))

		c.JSON(200, loc)
	})

	r.GET("/cars", func(c *gin.Context) {
		// Get Cars from Car Inventory
		resp, err := http.Get("http://roadrnd.westeurope.cloudapp.azure.com:5001/car")
		if err != nil {
			log.Fatalln(err)
		}
		body, err := ioutil.ReadAll(resp.Body)
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

	r.GET("/unlock/:car_id", func(c *gin.Context) {
		// Call Unlock Service to Unlock a certain Car
		values := map[string]string{"id": c.Param("car_id"), "tag": "tag1"}

		json_values, _ := json.Marshal(values)

		resp, err := http.Post("http://172.18.0.1:5003/unlock", "application/json", bytes.NewBuffer(json_values))
		if err != nil {
			log.Fatalln(err)
		}
		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatalln(err)
		}

		log.Println(body)

		c.String(http.StatusOK, "Car Unlocked")
	})

	r.GET("/lock/:car_id", func(c *gin.Context) {
		// Call Unlock Service to Unlock a certain Car
		values := map[string]string{"id": c.Param("car_id"), "tag": "tag1"}

		json_values, _ := json.Marshal(values)

		resp, err := http.Post("http://172.18.0.1:5003/lock", "application/json", bytes.NewBuffer(json_values))
		if err != nil {
			log.Fatalln(err)
		}
		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatalln(err)
		}

		log.Println(body)

		c.String(http.StatusOK, "Car Unlocked")
	})

	r.GET("/payment", func(c *gin.Context) {
		// Obtain required parameters to make request to payment service
		client_id := c.DefaultQuery("client_id", "123")
		transaction := c.DefaultQuery("transaction", "0")

		log.Println(client_id)
		log.Println(transaction)

		request_link := "http://roadrnd.westeurope.cloudapp.azure.com:5006/approve/PAYMENT-BDSk84729DHDSA7JDG6"

		c.String(http.StatusOK, request_link)
	})

	r.Run() // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
}
