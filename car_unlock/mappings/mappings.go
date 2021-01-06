// https://camellabs.com/gin-gonic-mysql-golang-example/
package mappings

import (
	"roadnd/car_unlock/controllers"

	"github.com/gin-gonic/gin"
)

func CreateMappings() *gin.Engine {
	r := gin.Default()

	r.POST("/unlock", controllers.UnlockCar)
	r.POST("/lock", controllers.LockCar)
	r.POST("/add", controllers.AddCar)
	r.POST("/delete", controllers.DelCar)
	r.POST("/updateTag", controllers.UpCarTag)
	r.GET("/clear", controllers.ClearDB)
	return r
}
