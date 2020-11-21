FROM golang:alpine

USER root

# RUN apt-get update
# RUN apt-get upgrade -y
RUN apk update
RUN apk add --no-cache git

RUN go get -u github.com/gin-gonic/gin

WORKDIR /app

COPY . .

RUN go build -o mainApp .

EXPOSE 8080

ENTRYPOINT ["./mainApp"]
# CMD tail -f /dev/null