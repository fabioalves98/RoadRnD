// https://camellabs.com/gin-gonic-mysql-golang-example/
// http://zetcode.com/golang/mysql/
package controllers

import (
	// "fmt"
	"io/ioutil"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
	_ "github.com/go-sql-driver/mysql"
)

type CAR struct {
	AT  string `json:"at" biding:"required"`
	ID  string `json:"id" biding:"required"`
	TAG string `json:"tag" biding:"required"`
}

func validateAT(AT string) bool {
	resp, err := http.Get("http://172.17.0.1:5005/validate_token/" + AT)

	if err != nil {
		log.Fatalln(err)
	}
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatalln(err)
	}
	log.Println(body)

	return resp.StatusCode == 200
}

func UnlockCar(c *gin.Context) {
	var car CAR
	c.BindJSON(&car)

	if car.TAG != "" && car.ID != "" && car.AT != "" {
		if validateAT(car.AT) {
			res, err := dbmap.Query("SELECT * FROM nfc WHERE tag = ?", car.TAG)
			defer res.Close()

			if err != nil {
				c.JSON(500, gin.H{"error": err})
			} else if res.Next() {
				var carDB CAR
				err := res.Scan(&carDB.ID, &carDB.TAG)

				if err != nil {
					c.JSON(500, gin.H{"error": err})
				}
				if car.ID == carDB.ID {
					c.JSON(200, gin.H{"message": "Car Unlocked", "car": carDB})
				} else {
					c.JSON(401, gin.H{
						"message":           "IDs don't match",
						"Received ID":       car.ID,
						"Tag associated ID": carDB.ID})
				}
			} else {
				c.JSON(400, gin.H{"error": "Tag not foung", "car": car})
			}
		} else {
			c.JSON(401, gin.H{"error": "Invalid Access Token", "car": car})
		}
	} else {
		c.JSON(400, gin.H{"error": "Empty fields", "car": car})
	}
}

func LockCar(c *gin.Context) {
	var car CAR
	c.BindJSON(&car)

	if car.TAG != "" && car.ID != "" && car.AT != "" {
		if validateAT(car.AT) {
			res, err := dbmap.Query("SELECT * FROM nfc WHERE tag = ?", car.TAG)
			defer res.Close()

			if err != nil {
				c.JSON(500, gin.H{"error": err})
			} else if res.Next() {
				var carDB CAR
				err := res.Scan(&carDB.ID, &carDB.TAG)

				if err != nil {
					c.JSON(500, gin.H{"error": err})
				} else if car.ID == carDB.ID {
					c.JSON(200, gin.H{"message": "Car Locked", "car": carDB})
				} else {
					c.JSON(401, gin.H{
						"message":           "IDs don't match",
						"Received ID":       car.ID,
						"Tag associated ID": carDB.ID})
				}
			} else {
				c.JSON(400, gin.H{"error": "Tag not foung", "car": car})
			}
		} else {
			c.JSON(401, gin.H{"error": "Invalid Access Token", "car": car})
		}
	} else {
		c.JSON(400, gin.H{"error": "Empty fields", "car": car})
	}
}

func AddCar(c *gin.Context) {
	var car CAR
	c.BindJSON(&car)

	// if car.TAG != "" && car.ID != "" && car.AT != "" {
	if car.ID != "" && car.TAG != "" {
		// if validateAT(car.AT) {
		if true { /* CHANGE TO VALIDATE ACCESS TOKEN */
			_, err := dbmap.Exec("INSERT INTO nfc(id,tag) VALUES (?,?)", car.ID, car.TAG)
			if err != nil {
				c.JSON(500, err)
			} else {
				c.JSON(201, gin.H{"message": "Car added", "car": car.ID})
			}
		} else {
			c.JSON(401, gin.H{"error": "Invalid Access Token", "car": car})
		}
	} else {
		c.JSON(400, gin.H{"error": "Empty fields", "car": car})
	}
}

func DelCar(c *gin.Context) {
	var car CAR
	c.BindJSON(&car)

	// if car.ID != "" && car.AT != "" {
	if car.ID != "" {
		// if validateAT(car.AT) {
		if true { /* CHANGE TO VALIDATE ACCESS TOKEN */
			_, err := dbmap.Exec("DELETE FROM nfc WHERE id = ?", car.ID)
			if err != nil {
				c.JSON(500, err)
			} else {
				c.JSON(201, gin.H{"message": "Car deleted", "car": car.ID})
			}
		} else {
			c.JSON(401, gin.H{"error": "Invalid Token", "car": car})
		}
	} else {
		c.JSON(400, gin.H{"error": "Empty fields", "car": car})
	}
}

func UpCarTag(c *gin.Context) {
	var car CAR
	c.BindJSON(&car)

	// if car.TAG != "" && car.ID != "" && car.AT != "" {
	if car.ID != "" && car.TAG != "" {
		// if validateAT(car.AT) {
		if true { /* CHANGE TO VALIDATE ACCESS TOKEN */
			_, err := dbmap.Exec("UPDATE nfc SET tag = ? WHERE id = ?", car.TAG, car.ID)
			if err != nil {
				c.JSON(500, err)
			} else {
				c.JSON(201, gin.H{"message": "Car Updated", "car": car.ID, "new tag": car.TAG})
			}
		} else {
			c.JSON(401, gin.H{"error": "Invalid Token", "car": car})
		}
	} else {
		c.JSON(400, gin.H{"error": "Empty fields", "car": car})
	}
}

func ClearDB(c *gin.Context) {
	_, err := dbmap.Exec("DELETE FROM nfc")
	if err != nil {
		c.JSON(500, err)
	} else {
		c.JSON(200, gin.H{"message": "NFC Database clear"})
	}
}
