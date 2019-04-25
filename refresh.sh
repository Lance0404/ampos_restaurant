#!/bin/bash

# chmod +x *.py *.sh
dropdb=$1
# example: ./refresh.sh drop
echo "dropdb param: $dropdb"
docker-compose down -v
docker-compose build
# create external volumn
if [ "$dropdb" == "drop" ]; then
    docker volume rm ar_pgdata
    docker volume create --name=ar_pgdata
    docker-compose up -d
    sleep 5 # takes time for containter be ready
    # ------------------ START init DB ------------------
    # psql -h localhost -p 5433 -U postgres -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'ampos' AND pid <> pg_backend_pid()"
    # psql -h localhost -p 5433 -U postgres -c 'DROP DATABASE ampos'
    # psql -h localhost -p 5433 -U postgres -c 'CREATE DATABASE ampos'
    docker exec -it ar_psql psql -h localhost -U postgres -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'ampos' AND pid <> pg_backend_pid()"
    docker exec -it ar_psql psql -h localhost -U postgres -c 'DROP DATABASE ampos'
    docker exec -it ar_psql psql -h localhost -U postgres -c 'CREATE DATABASE ampos'    
    # ------------------ END ------------------
else
    docker exec -it ar_psql psql -h localhost -U postgres -c 'CREATE DATABASE ampos'  
    docker-compose up -d
fi

docker rmi $(docker images -f "dangling=true" -q)
docker-compose ps
# python manage.py shell
curl -v -X GET 'http://localhost:8900/v1/test'
