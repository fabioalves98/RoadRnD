FROM golang:latest AS build
# FROM micro/micro:latest AS build

RUN apt-get update
RUN apt-get upgrade -y

# ENV GOBIN /go/bin
WORKDIR /src/
COPY main.go go.* /src/
RUN go get github.com/golang/protobuf/protoc-gen-go
RUN go get github.com/micro/micro/v3/cmd/protoc-gen-micro

RUN CGO_ENABLED=0 go build -o /bin/demo

