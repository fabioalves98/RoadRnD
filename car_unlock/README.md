# Car-Unlock Microservice
Microservice using nfc tags to unlock a car using it's license plate as ID.

## HOW TO RUN
Run "start.sh" script and a docker container is created and running in port 5673
Run "delete.sh" to delete all the images and the container.

```properties
# POST command to unlock car:
curl -i -X POST http://localhost:5673/unlock -H "Accept: application/json" "Content-Type: application/json" -d '{"id":"10-20-XX", "tag":"nfc Tag"}'

# POST command to lock car:
curl -i -X POST http://localhost:5673/lock -H "Accept: application/json" "Content-Type: application/json" -d '{"id":"10-20-XX", "tag":"nfc Tag"}'

# POST command to add car:
curl -i -X POST http://localhost:5673/add -H "Accept: application/json" "Content-Type: application/json" -d '{"id":"10-20-XX"}'
```