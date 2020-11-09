#!/bin/bash
imageName=roadrnd:comp
containerName=rnd_comp

docker build -t $imageName -f Dockerfile  .

echo Delete old container...
docker rm -f $containerName

echo Run new container...
docker run --name $containerName -d -v ${PWD}:/app -p 5000:8080 $imageName