#!/bin/bash

gnome-terminal -- bash -c "pwd; echo server ; source .env/bin/activate ; python -m cortex.server run-server; bash"
gnome-terminal -- bash -c "pwd; echo saver ; source .env/bin/activate ; python -m cortex.saver run-saver ; bash"
gnome-terminal -- bash -c "pwd; echo pose ; source .env/bin/activate ; python -m cortex.parsers run-parser 'pose' ; bash"
gnome-terminal -- bash -c "pwd; echo feelings ; source .env/bin/activate ; python -m cortex.parsers run-parser 'feelings' ; bash"
gnome-terminal -- bash -c "pwd; echo color_image ; source .env/bin/activate ; python -m cortex.parsers run-parser 'color_image' ; bash"
gnome-terminal -- bash -c "pwd; echo depth_image;  source .env/bin/activate ; python -m cortex.parsers run-parser 'depth_image' ; bash"
gnome-terminal -- bash -c "pwd; echo api; source .env/bin/activate ; python -m cortex.api run-server ; bash"
gnome-terminal -- bash -c "pwd; echo gui ; source .env/bin/activate ; python -m cortex.gui run-server ; bash"
gnome-terminal -- bash -c "pwd; echo client ; source .env/bin/activate ; python -m cortex.client upload-sample ; bash"