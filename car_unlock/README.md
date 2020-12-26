# Car-Unlock Microservice
Microservice using nfc tags to unlock a car using it's license plate as ID.

## HOW TO RUN
docker-compose build
docker-compose up

[Link to API](https://app.swaggerhub.com/apis-docs/MSilva98/CarUnlock/1.0.0)

```properties
# POST command to unlock car:
curl -i -X POST http://localhost:5003/unlock -H "Accept: application/json" "Content-Type: application/json" -d '{"at":"suahaiui7862", "id":"AA-01-AA", "tag":"tag1"}'

# POST command to lock car:
curl -i -X POST http://localhost:5003/lock -H "Accept: application/json" "Content-Type: application/json" -d '{"at":"suahaiui7862", "id":"AA-01-AA", "tag":"tag1"}'

# POST command to add car:
curl -i -X POST http://localhost:5003/add -H "Accept: application/json" "Content-Type: application/json" -d '{"at":"suahaiui7862", "id":"CD-55-23", "tag": "tagX"}'

# POST command to update car tag:
curl -i -X POST http://localhost:5003/updateTag -H "Accept: application/json" "Content-Type: application/json" -d '{"at":"suahaiui7862", "id":"CD-55-23", "tag": "tagV2"}'

# POST command to delete car:
curl -i -X POST http://localhost:5003/delete -H "Accept: application/json" "Content-Type: application/json" -d '{"at":"suahaiui7862", "id":"CD-55-23"}'
```