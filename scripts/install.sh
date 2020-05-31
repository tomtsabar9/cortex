#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."

apt-get update
pip3.8 install virtualenv
apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker

apt-get install gnome-terminal 

function main {
    python3.8 -m virtualenv .env --prompt "[cortex] "
    find .env -name site-packages -exec bash -c 'echo "../../../../" > {}/self.pth' \;
    .env/bin/pip install -U pip
    .env/bin/pip install -r requirements.txt
}
 
chmod +x ./scripts/run_pipeline.sh
main "$@"
