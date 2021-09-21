#!/bin/bash

if [ $# -eq 0 ]
    then
        docker-compose up
        exit 0
fi

if [ "$1" = "build" ]
    then
        docker-compose up --build
        exit 0
fi

if [ "$1" = "args" ]
    then
        docker-compose up ${@:2}
        exit 0
fi

echo "Usage:"
echo $0 "           Starts the required images using docker compose"
echo $0 "build      Builds and starts the required images using docker compose"
echo $0 "args       Allows for the passing of additional flags to docker compose"