gnome-terminal --title="Server" -- bash -c "pwd; source .env/bin/activate ; python -m cortex.server run-server"
gnome-terminal --title="Client" -- bash -c "pwd; source .env/bin/activate ; python -m cortex.client run-server"
gnome-terminal --title="Saver" -- bash -c "pwd; source .env/bin/activate ; python -m cortex.saver run-server"
gnome-terminal --title="Pose parser" -- bash -c "pwd; source .env/bin/activate ; python -m cortex.parsers run-parser 'pose'"
gnome-terminal --title="Feelings parser" -- bash -c "pwd; source .env/bin/activate ; python -m cortex.parsers run-parser 'feelings'"
gnome-terminal --title="Color_image parser" -- bash -c "pwd; source .env/bin/activate ; python -m cortex.parsers run-parser 'color_image'"
gnome-terminal --title="Depth_image parser" -- bash -c "pwd; source .env/bin/activate ; python -m cortex.parsers run-parser 'depth_image'"
gnome-terminal --title="API" -- bash -c "pwd; source .env/bin/activate ; python -m cortex.api run-server"
gnome-terminal --title="GUI" -- bash -c "pwd; source .env/bin/activate ; python -m cortex.gui run-server"