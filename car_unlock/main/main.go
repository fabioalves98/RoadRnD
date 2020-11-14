// https://github.com/gin-gonic/gin#querystring-parameters
// https://camellabs.com/gin-gonic-mysql-golang-example/
package main

import (
	"roadnd/car_unlock/mappings"
	_ "github.com/go-sql-driver/mysql"
)	

func main() {
	r := mappings.CreateMappings()
	r.Run(":5673") // listen and serve on 0.0.0.0:5673 (for windows "localhost:5673")
}
