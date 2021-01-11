package main

import (
	"bytes"
	"encoding/json"
	"fmt"
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

type Credentials struct {
	Auth_code string
	Client_id string
	Image     string
	Mail      string
	User_key  string
	User_name string
}

type Token struct {
	Access_token string
	Token_type   string
}

type PaymentInfo struct {
	CarID string
	Price string
}

type PaymentID struct {
	Payment_id string
}

//var docker_internal_ip = "http://172.22.0.1"
// docker vm ip
var docker_internal_ip = "http://172.17.0.1"
var vm_ip = "http://roadrnd.westeurope.cloudapp.azure.com"

func main() {
	r := gin.Default()

	r.GET("/login", func(c *gin.Context) {
		// Obtain required parameters to make request to OAuth service
		client_id := c.DefaultQuery("client_id", "RoadRnD")

		log.Println(client_id)

		// Make request to OAuth Server
		request_link := vm_ip + ":5005/oauth/authorize?client_id=RoadRnD&redirect_url=http://www.roadrnd.com&user_key=D1234D"
		c.String(http.StatusOK, request_link)
	})

	r.GET("/credentials", func(c *gin.Context) {
		// Get credentials from OAuth service
		credentials_link := vm_ip + ":5005/oauth/credentials?user_key=D1234D"
		resp, err := http.Get(credentials_link)
		if err != nil {
			log.Fatalln(err)
		}
		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatalln(err)
		}

		var cred []Credentials
		err = json.Unmarshal([]byte(body), &cred)

		if err != nil {
			log.Println("Error Parsing Inventory JSON data - ", err)
		}

		pretty_inv, err := json.MarshalIndent(cred, "", "    ")
		log.Println(string(pretty_inv))

		// Get Token from OAuth service
		token_link := vm_ip + ":5005/oauth/token?client_id=RoadRnD&redirect_url=http://www.roadrnd.com&authorization_code=" + cred[0].Auth_code
		resp, err = http.Get(token_link)
		if err != nil {
			log.Fatalln(err)
		}
		body, err = ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatalln(err)
		}

		var token Token
		err = json.Unmarshal([]byte(body), &token)

		if err != nil {
			log.Println("Error Parsing Inventory JSON data - ", err)
		}

		pretty_inv, err = json.MarshalIndent(token, "", "    ")
		log.Println(string(pretty_inv))

		c.String(200, token.Access_token)

	})

	r.GET("/map", func(c *gin.Context) {
		// Get Car location from Car Location
		resp, err := http.Get(docker_internal_ip + ":5002/car")
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

		log.Println(len(loc))

		pretty_loc, err := json.MarshalIndent(loc, "", "    ")
		log.Println(string(pretty_loc))

		c.JSON(200, loc)
	})

	r.GET("/cars", func(c *gin.Context) {
		// Get Token from header
		token := c.Request.Header["Authorization"]
		log.Println(token)

		url := docker_internal_ip + ":5001/car"

		var jsonStr = []byte("{\"access_token\": \"" + token[0] + "\"}")
		req, err := http.NewRequest("GET", url, bytes.NewBuffer(jsonStr))
		req.Header.Set("Content-Type", "application/json")

		client := &http.Client{}
		resp, err := client.Do(req)
		if err != nil {
			panic(err)
		}
		defer resp.Body.Close()

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

		log.Println(len(cars))

		pretty_inv, err := json.MarshalIndent(cars, "", "    ")
		log.Println(string(pretty_inv))

		c.JSON(200, cars)
	})

	r.GET("/car/:id", func(c *gin.Context) {
		id := c.Param("id")

		// Get Token from header
		token := c.Request.Header["Authorization"]
		log.Println(token)

		url := docker_internal_ip + ":5001/car/" + id

		var jsonStr = []byte("{\"access_token\": \"" + token[0] + "\"}")
		req, err := http.NewRequest("GET", url, bytes.NewBuffer(jsonStr))
		req.Header.Set("Content-Type", "application/json")

		client := &http.Client{}
		resp, err := client.Do(req)
		if err != nil {
			panic(err)
		}
		defer resp.Body.Close()

		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatalln(err)
		}

		// Convert to Car Structure
		var car []Car
		err = json.Unmarshal([]byte(body), &car)

		if err != nil {
			log.Println("Error Parsing Inventory JSON data - ", err)
		}

		pretty_inv, err := json.MarshalIndent(car, "", "    ")
		log.Println(string(pretty_inv))

		c.JSON(200, car[0])

	})

	r.POST("/create_payment", func(c *gin.Context) {
		log.Println("Create Payment endpoint")

		// Get Token from header
		token := c.Request.Header["Authorization"]
		log.Println(token)

		// Obtain payment info from app
		body, err := ioutil.ReadAll(c.Request.Body)
		if err != nil {
			panic(err)
		}

		var paymentInfo PaymentInfo
		err = json.Unmarshal([]byte(body), &paymentInfo)
		if err != nil {
			log.Println("Error Parsing Inventory JSON data - ", err)
		}

		pretty, err := json.MarshalIndent(paymentInfo, "", "    ")
		log.Println(string(pretty))

		// Make POST request to payment service to obtain payment link
		url := "http://roadrnd.westeurope.cloudapp.azure.com:5006/payment"

		var jsonStr = []byte("{\"client_id\": \"1234567\", \"access_token\": \"" + token[0] +
			"\", \"transaction\" : {\"total\" : \"" + paymentInfo.Price +
			"\", \"currency\": \"EUR\"}, \"item_list\" : [{\"item_name\": \"Rental - " +
			paymentInfo.CarID + "\",\"item_price\" : \"" + paymentInfo.Price + "\"}]}")
		req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonStr))
		req.Header.Set("Content-Type", "application/json")

		client := &http.Client{}
		resp, err := client.Do(req)
		if err != nil {
			panic(err)
		}
		defer resp.Body.Close()

		fmt.Println("response Status:", resp.Status)
		fmt.Println("response Headers:", resp.Header)
		body, _ = ioutil.ReadAll(resp.Body)
		fmt.Println("response Body:", string(body))

		var pay PaymentID
		err = json.Unmarshal([]byte(body), &pay)

		if err != nil {
			log.Println("Error Parsing Inventory JSON data - ", err)
		}

		c.String(http.StatusOK, pay.Payment_id)
	})

	r.Run() // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
}
