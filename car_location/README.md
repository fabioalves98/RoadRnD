## Endpoints


`/car GET (All cars)`

```javascript
/car POST (Body params) 
{
    "location" : "41.40338, 2.17403"
    "status"   : "Parked"
}
```


`/car_location/{car_id} GET (specific car)`

```javascript
/car_location/{car_id} PUT (body params with the updated fields)
{
    "location" : "41.40338, 2.17403"
}
```


`/car_status/{car_id} GET`

```javascript
/car_status/{car_id} PUT
{
    "status"   : "Parked"
}
```

