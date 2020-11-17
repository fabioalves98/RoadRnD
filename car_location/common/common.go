package common

import "fmt"
// "database/sql"
// _"github.com/lib/pq"
// "./main"
// )

type CarLocation struct{	
	Car_id 		string `json:"car_id"`
	Location 	string `json:"location"`
	Status 		string `json:"status"`
}

type Location struct{
	Coords 	string `json:"location"`
	Radius  int    `json:"radius"`
}


func Check(err error, msg string) bool{
	if err != nil {
		fmt.Printf(msg)
		fmt.Println(err.Error())	
		return false
	}
	return true
}