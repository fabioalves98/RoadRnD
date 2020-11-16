FROM golang:latest AS build
# # FROM micro/micro:latest AS build

USER root

RUN apt-get update
RUN apt-get upgrade -y

RUN go get -u -x github.com/gin-gonic/gin
RUN go get -u -x github.com/lib/pq
WORKDIR /src/
COPY main.go go.* /src/
ADD database /src/database
ADD common /src/common
RUN ls

RUN CGO_ENABLED=0 go build -o /bin/app

FROM scratch
COPY --from=build /bin/app /bin/app
ENTRYPOINT ["/bin/app"]

