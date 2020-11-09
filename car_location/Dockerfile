FROM golang:latest AS build
# # FROM micro/micro:latest AS build

USER root

RUN apt-get update
RUN apt-get upgrade -y

RUN go get -u -x github.com/gin-gonic/gin
RUN go get -u -x github.com/lib/pq
WORKDIR /src/
COPY main.go go.* /src/
# RUN go get github.com/eclipse/paho.mqtt.golang


RUN CGO_ENABLED=0 go build -o /bin/demo

FROM scratch
COPY --from=build /bin/demo /bin/demo
ENTRYPOINT ["/bin/demo"]

