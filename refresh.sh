#!/bin/bash
echo $1
if [ "$1" = "dev" ]; then
    echo "Refreshing local"
    docker-compose down && docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
else
    echo "Refreshing production"
    docker-compose down && docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
fi
