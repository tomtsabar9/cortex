#!/bin/bash
 
if [ $# -ne 2 ]
  then
    echo "Please supply email and password"
    exit 1
fi

echo $1
echo $2

docker pull rabbitmq
docker run -d --name some-rabbit -p 4369:4369 -p 5671:5671 -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=$1 -e RABBITMQ_DEFAULT_PASS=$2 rabbitmq
docker exec some-rabbit rabbitmq-plugins enable rabbitmq_management
docker start some-rabbit
docker pull postgres
docker run -p 5432:5432 --name some-postgres -e POSTGRES_USER=$1 -e POSTGRES_PASSWORD=$2 -d postgres
docker start some-postgres
docker pull dpage/pgadmin4
docker run -p 80:80 --name some-postgres-admin -e PGADMIN_DEFAULT_EMAIL=$1 -e PGADMIN_DEFAULT_PASSWORD=$2 -d dpage/pgadmin4
docker start some-postgres-admin