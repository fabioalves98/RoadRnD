// https://github.com/gin-gonic/gin#querystring-parameters
package main

import (
	"github.com/gin-gonic/gin"
)	

type ADD struct {
	ID string `json:"id" biding:"required"`
}

type CAR struct {
	ID string `json:"id" biding:"required"`
	TAG string `json:"tag" biding:"required"`
}

func main() {
	r := gin.Default()

	// r.LoadHTMLFiles("templates/nfc.html")

	// curl -i -X POST http://localhost:5673/unlock -H "Accept: application/json" "Content-Type: application/json" -d '{"id":"3", "tag":"adacas"}'
	r.POST("/unlock", func(c *gin.Context) {
		var car CAR
		c.BindJSON(&car)
		c.JSON(200, gin.H{"car plate": car.ID, "nfc tag": car.TAG})
	})

	// curl -i -X POST http://localhost:5673/lock -H "Accept: application/json" "Content-Type: application/json" -d '{"id":"3", "tag":"adacas"}'
	r.POST("/lock", func(c *gin.Context) {
		var car CAR
		c.BindJSON(&car)
		c.JSON(200, gin.H{"car plate": car.ID, "nfc tag": car.TAG, "carlocked":1})
	})

	// r.GET("/lock/:id", func(c *gin.Context) {
	// 	id := c.Param("id")
	// 	// c.HTML(200, "nfc.html", gin.H{"title": "NFC reader"})
	// 	c.JSON(200, gin.H{"car plate": id})
	// })
	
	// https://github.com/gin-gonic/gin/issues/424
	// curl -i -X POST http://localhost:5673/add -H "Accept: application/json" "Content-Type: application/json" -d '{"id":"3"}'
	r.POST("/add", func(c *gin.Context) {
		var car ADD
		c.BindJSON(&car)
		c.JSON(200, gin.H{"message": car.ID})
		// fmt.Println("Car plate:", car.ID)
	})

	r.Run(":5673") // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
}
