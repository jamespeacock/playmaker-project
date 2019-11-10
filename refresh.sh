#!/bin/bash
echo $1
if [ "$1" = "dev" ]; then
    echo "Refreshing local"
    docker-compose down && docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
else
    echo "Refreshing production"
    if [ "$2" = "build" ]; then
        docker-compose down && docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
        docker exec -it interface python3.6 manage.py migrate
    else
        docker-compose down && docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
    fi
fi
