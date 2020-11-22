## Endpoints

### Create a new payment
`/create POST e.g. Body params`
```javascript
{
    "transaction"   : {
        "total" : "24.90",
        "currency" : "USD"  // or others like EUR
    },
    "item_list" : [
        {
            "item_name" : "Car rental",
            "item_price" : "12.90",
            "item_tax": "0.24"
        },
        {
            "item_name" : "Other car rental",
            "item_price" : "15.30",
            "item_tax": "0.54"
        }
    ]
}
```
### Example
```bash
curl --header "Content-Type: application/json"   --request POST   --data '{"transaction" : {"total" : "24.90", "currency": "USD"}, "invoice_number" : "8394839284", "item_list" : [{"item_name": "Car Rental", "item_price" : "12.90", "item_tax" : "0.24"}, {"item_name": "Car Rental", "item_price" : "12.00", "item_tax" : "0.20"}]}'   http://0.0.0.0:5006/create
```

#### Returns
```javascript
{
    "id": "PAYMENT-BDSk84729DHDSA7JDG6",
    "create_time": "2020-11-02T19:32:10",
    "update_time": "2020-11-02T19:32:10",
    "state": "created"
}
```

## Execute the payment
`/execute POST e.g. Body params`
```javascript
{
    "access_token" : "321hDSAj325jDSAK897SA"
    "payment_id"   : "PAYMENT-BDSk84729DHDSA7JDG6"
}
```

### Returns
```javascript
{
    "payment_id"   : "PAYMENT-BDSk84729DHDSA7JDG6",
    "create_time": "2020-11-02T19:32:10",
    "update_time": "2020-11-02T19:37:23",
    "state": "approved"
}
```


# Service flow
1. User clicks the app "Payment" button. (app calls /create)
2. A payment webpage with all the items provided in item list is presented to the user.
3. User approves the purchase with a button inside this webpage. (/execute)
4. Verify access token, check payment_id info and proceed with the payment.
