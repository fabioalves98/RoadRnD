
## App service flow
1. Call /payment payment (with at least 1 item in item_list) 
2. Call /approve with the returned payment_id from /create
3. When the user completes the payment the /execute is internally called
4. Call /payment/<payment_id> with the previously mentioned id to check the payment status

## Crud endpoints for payments
`/payment/<payment_id> GET`
`/payment/<payment_id> DELETE`
`/payment POST (body params -> shown bellow)`

## Crud endpoints for clients and balance
`/client/<payment_id> GET`
`/client/<payment_id> PUT (body params -> {"balance": <funds_to_be_added>)`
`/client POST (body params -> {"id": client_id, "currency": "EUR"}`

## Flow Endpoints

### Create a new payment
`/payment POST e.g. Body params`
```javascript
{
    "client_id" : "1234567",
    "access_token" : "i32o1531ioh3o1ih321oih",
    "transaction"   : {
        "total" : "24.90",
        "currency" : "EUR"  // or others like EUR
    },
    "item_list" : [
        {
            "item_name" : "Rental",
            "item_price" : "24.90",
        }
    ]
}
```
### Example
```bash
curl --header "Content-Type: application/json"   --request POST   --data '{"client_id": "LD-34-CV", "transaction" : {"total" : "24.90", "currency": "EUR"}, "item_list" : [{"item_name": "Rental", "item_price" : "24.90"}]}'   http://0.0.0.0:5006/payment
```

### Returns
```javascript
{
    "payment_id"   : "PAYMENT-BDSk84729DHDSA7JDG6"
}
```

## Approve payment
When the /create endpoint is called the user is automatically redirected to /approve/<payment_id>
### Example
```bash
# In a browser:
0.0.0.0:5006/approve/PAYMENT-BDSk84729DHDSA7JDG6
```

## Execute the payment (This is called internally by the payment service)
`/execute POST e.g. Body params`
```javascript
{
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
