#!/bin/bash

gnome-terminal --title="Server" -- bash -c "pwd; source .env/bin/activate ; python -m cortex.server run-server; bash"
gnome-terminal --title="Saver" -- bash -c "pwd; source .env/bin/activate ; python -m cortex.saver run-saver ; bash"
gnome-terminal --title="Pose parser" -- bash -c "pwd; source .env/bin/activate ; python -m cortex.parsers run-parser 'pose' ; bash"
gnome-terminal --title="Feelings parser" -- bash -c "pwd; source .env/bin/activate ; python -m cortex.parsers run-parser 'feelings' ; bash"
gnome-terminal --title="Color_image parser" -- bash -c "pwd; source .env/bin/activate ; python -m cortex.parsers run-parser 'color_image' ; bash"
gnome-terminal --title="Depth_image parser" -- bash -c "pwd; source .env/bin/activate ; python -m cortex.parsers run-parser 'depth_image' ; bash"
gnome-terminal --title="API" -- bash -c "pwd; source .env/bin/activate ; python -m cortex.api run-server ; bash"
gnome-terminal --title="GUI" -- bash -c "pwd; source .env/bin/activate ; python -m cortex.gui run-server ; bash"
gnome-terminal --title="Client" -- bash -c "pwd; source .env/bin/activate ; python -m cortex.client upload-sample ; bash"