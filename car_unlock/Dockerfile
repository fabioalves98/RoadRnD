FROM golang:alpine

WORKDIR /src/
COPY go.* /src/
ADD controllers /src/controllers
ADD main /src/main
ADD mappings /src/mappings

RUN apk update
RUN apk add --no-cache git

RUN go get -u github.com/gin-gonic/gin
RUN go get -u github.com/go-sql-driver/mysql

RUN go build -o mainApp ./main/main.go

ENTRYPOINT ["./mainApp"]
