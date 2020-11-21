FROM golang:alpine AS build

USER root

RUN apk update
RUN apk add --no-cache git

RUN go get -u -x github.com/gin-gonic/gin
RUN go get -u -x github.com/lib/pq
RUN go get -u -x github.com/cridenour/go-postgis
RUN go get -u github.com/paulmach/orb/encoding/wkb
WORKDIR /src/
COPY main.go go.* /src/
ADD database /src/database
ADD common /src/common

RUN CGO_ENABLED=0 go build -o /bin/app

FROM scratch
COPY --from=build /bin/app /bin/app
ENTRYPOINT ["/bin/app"]

