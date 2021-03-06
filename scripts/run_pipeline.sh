#!/bin/bash
if [ $# -ne 2 ]
  then
    echo "Please supply username and password"
    exit 1
fi

apt-get update
apt install docker.io
systemctl start docker
systemctl enable docker

apt-get install gnome-terminal 

export _USERNAME=$1 
export _PASSWORD=$2

chmod +x ./scripts/start_dockers.sh
chmod +x ./scripts/rm_dockers.sh

./scripts/start_dockers.sh $1 $2

chmod +x ./scripts/start_micro_services.sh

./scripts/start_micro_services.sh

