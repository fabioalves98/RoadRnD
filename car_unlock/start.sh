#!/bin/bash
app="car_unlock"
docker build -t ${app} .
docker run -p 5673:5673 --name=${app} -d ${app}