#!/bin/bash

# chmod +x *.py *.sh
dropdb=$1
# example: ./refresh.sh drop
echo "dropdb param: $dropdb"
docker-compose down -v
docker-compose build
# create external volumn
if [ "$dropdb" == "drop" ]; then
    # docker volume create --name=pgdata
    # ------------------ START init DB ------------------
    psql -h localhost -U postgres -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'ampos' AND pid <> pg_backend_pid()"
    psql -h localhost -U postgres -c 'DROP DATABASE ampos'
    psql -h localhost -U postgres -c 'CREATE DATABASE ampos'
    # ------------------ END ------------------
else
    psql -h localhost -U postgres -c 'CREATE DATABASE ampos'
fi
docker-compose up -d
docker rmi $(docker images -f "dangling=true" -q)
docker-compose ps
curl -v -X GET 'http://localhost:8900/v1/test'

