## Endpoints


`/car GET (All cars)`

`/car/{car_id} POST (Body params)` 
```javascript
{
    "location" : "41.40338, 2.17403"
    "status"   : "Parked"
}
```
Example: 
```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"location" : "41.40338, 2.17403", "status"   : "Parked"}' \
  http://0.0.0.0:8080/car/AA-01-AA
```



`/car_location/{car_id} GET (specific car)`

`/car_location/{car_id} PUT (body params with the updated fields)`
```javascript
{
    "location" : "41.40338, 2.17403"
}
```


`/car_status/{car_id} GET`


`/car_status/{car_id} PUT`
```javascript
{
    "status"   : "Parked"
}


```

