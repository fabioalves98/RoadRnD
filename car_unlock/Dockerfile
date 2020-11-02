FROM golang:alpine

WORKDIR /src
COPY ./main.go .

RUN apk update
RUN apk add --no-cache git

RUN go get -u github.com/gin-gonic/gin
RUN go build -o main .

EXPOSE 5673

ENTRYPOINT ["./main"]
