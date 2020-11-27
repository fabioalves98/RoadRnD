## Endpoints

### Create a new payment
`/create POST e.g. Body params`
```javascript
{
    "client_id" : "AA-01-AA", // The id used by car_inventory service or the car plate nr
    "transaction"   : {
        "total" : "24.90",
        "currency" : "USD"  // or others like EUR
    },
    "item_list" : [
        {
            "item_name" : "Rental",
            "item_price" : "12.90",
        },
        {
            "item_name" : "Rental",
            "item_price" : "15.30",
        }
    ]
}
```
### Example
```bash
curl --header "Content-Type: application/json"   --request GET   --data '{"client_id": "LD-34-CV", "transaction" : {"total" : "24.90", "currency": "USD"}, "invoice_number" : "8394839284", "item_list" : [{"item_name": "Rental", "item_price" : "12.90"}, {"item_name": "Rental", "item_price" : "12.00"}]}'   http://0.0.0.0:5006/create
```

## Approve payment
When the /create endpoint is called the user is automatically redirected to /approve/<payment_id>
### Example
```bash
# In a browser:
0.0.0.0:5006/approve/PAYMENT-BDSk84729DHDSA7JDG6
```

## Execute the payment
`/execute POST e.g. Body params`
```javascript
{
    "access_token" : "321hDSAj325jDSAK897SA" // and credit card data or something depending on payment method?
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
4. Verify access token (or credit card data or something), check payment_id info and proceed with the payment.
