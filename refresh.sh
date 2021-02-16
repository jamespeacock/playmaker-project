#!/bin/bash
echo $1
if [ "$1" = "dev" ]; then
    echo "Refreshing local"
    if [ "$2" = "build" ]; then
        docker-compose down && docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d
    else
        docker-compose down && docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
    fi
else
    echo "Refreshing production"
    if [ "$1" = "build" ]; then
        docker-compose down && docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
        docker exec -it interface python3.8 manage.py migrate
    else
        docker-compose down && docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
    fi
fi
