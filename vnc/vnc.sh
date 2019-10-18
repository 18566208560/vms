#! /bin/sh
sudo cp ./vnc.pass /etc/
sudo cp ./x11vnc.service /usr/lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start x11vnc


