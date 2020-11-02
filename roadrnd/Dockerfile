FROM golang:latest

USER root

RUN apt-get update
RUN apt-get upgrade -y

RUN go get -u github.com/gin-gonic/gin

WORKDIR /app

COPY . .

RUN go build -o main .

EXPOSE 8080

# CMD [ "./main" ]
CMD tail -f /dev/null