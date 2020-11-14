// https://camellabs.com/gin-gonic-mysql-golang-example/
// http://zetcode.com/golang/mysql/
package controllers

import (
	"database/sql"
	"log"
	"github.com/gin-gonic/gin"
	_ "github.com/go-sql-driver/mysql"
)

var dbmap = initDb()

func initDb() (db *sql.DB){
	db, err := sql.Open("mysql", "car_unlock:car_unlock@tcp(sql_db:3306)/unlockDB")
	if err != nil {
		log.Fatalln("SQL Open failed ", err)
	}
	return db
}

func Cors() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Add("Access-Control-Allow-Origin", "*")
		c.Next()
	}
}