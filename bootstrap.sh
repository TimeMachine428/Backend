#!/bin/bash

docker-compose down
docker volume rm backend_db-data
docker volume create backend_db-data
docker network create backend_default
# docker-compose pull
# docker-compose build
docker-compose create
docker-compose start mysql

echo "Waiting for mysql database to be initialized..."
while [ 1 ]; do
    curl --silent --output /dev/null localhost:3306
    if [ $? -eq 0 ]; then
        break;
    fi
done

python timemachine/manage.py migrate

echo "Creating an admin user for the administrator interface..."
python timemachine/manage.py createsuperuser

docker-compose start

echo "Everything should be running now..."