// https://camellabs.com/gin-gonic-mysql-golang-example/
// http://zetcode.com/golang/mysql/
package controllers

import (
	// "log"
	// "fmt"
	"github.com/gin-gonic/gin"
	_ "github.com/go-sql-driver/mysql"
)

type CAR struct {
	ID string `json:"id" biding:"required"`
	TAG string `json:"tag" biding:"required"`
}

func UnlockCar(c *gin.Context) {
	var car CAR
	c.BindJSON(&car)

	if car.TAG != "" && car.ID != "" {
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
			if car.ID == carDB.ID{
				c.JSON(200, gin.H{"message": "Car Unlocked", "car": carDB})
			} else {
				c.JSON(401, gin.H{
					"message": "IDs don't match", 
					"Received ID": car.ID, 
					"Tag associated ID": carDB.ID})
			}
		} else {
			c.JSON(400, gin.H{"error": "Tag not foung", "car": car})	
		}
	} else {
		c.JSON(400, gin.H{"error": "Empty fields", "car": car})	
	}
}

func LockCar(c *gin.Context) {
	var car CAR
	c.BindJSON(&car)
	
	if car.TAG != "" && car.ID != "" {
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
					"message": "IDs don't match", 
					"Received ID": car.ID, 
					"Tag associated ID": carDB.ID})
			}
		} else {
			c.JSON(400, gin.H{"error": "Tag not foung", "car": car})	
		}
	} else {
		c.JSON(400, gin.H{"error": "Empty fields", "car": car})	
	}
}

func AddCar(c *gin.Context) {
	var car CAR
	c.BindJSON(&car)
	
	if car.ID != "" && car.TAG != "" {
		_, err := dbmap.Exec("INSERT INTO nfc(id,tag) VALUES (?,?)", car.ID, car.TAG)
		if err != nil {
			c.JSON(500, err)
		} else {
			c.JSON(201, gin.H{"message": "Car added", "car": car.ID})
		}
	} else{
		c.JSON(400, gin.H{"error": "Empty fields", "car": car})	
	}
}

func DelCar(c *gin.Context) {
	var car CAR
	c.BindJSON(&car)

	if car.ID != "" {
		_, err := dbmap.Exec("DELETE FROM nfc WHERE id = ?", car.ID)
		if err != nil {
			c.JSON(500, err)
		} else {
			c.JSON(201, gin.H{"message": "Car deleted", "car": car.ID})
		}
	} else {
		c.JSON(400, gin.H{"error": "Empty fields", "car": car})	
	}	
}

func UpCarTag(c *gin.Context) {
	var car CAR
	c.BindJSON(&car)
	
	if car.ID != "" && car.TAG != "" {
		_, err := dbmap.Exec("UPDATE nfc SET tag = ? WHERE id = ?", car.TAG, car.ID)
		if err != nil {
			c.JSON(500, err)
		} else {
			c.JSON(201, gin.H{"message": "Car Updated", "car": car.ID, "new tag": car.TAG})
		}
	} else{
		c.JSON(400, gin.H{"error": "Empty fields", "car": car})	
	}
}