#!/bin/bash

docker pull rabbitmq
docker run -d --name some-rabbit -p 4369:4369 -p 5671:5671 -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=tomtsabar9@gmail.com -e RABBITMQ_DEFAULT_PASS=mysecretpassword rabbitmq
docker exec some-rabbit rabbitmq-plugins enable rabbitmq_management
docker start some-rabbit
docker pull postgres
docker run -p 127.0.0.1:5432:5432 --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d tomtsabar9@gmail.com
docker start some-postgres
docker pull dpage/pgadmin4
docker run -p 80:80 --name some-postgres-admin -e 'PGADMIN_DEFAULT_EMAIL=tomtsabar9@gmail.com' -e 'PGADMIN_DEFAULT_PASSWORD=mysecretpassword' -d dpage/pgadmin4
docker start some-postgres-admin