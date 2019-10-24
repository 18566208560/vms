#! /bin/sh


if [ ! -f /etc/vnc.pass ];then
    sudo cp ./vnc.pass /etc/
fi

if [ ! -f /usr/lib/systemd/system/x11vnc.service ]:then
    sudo cp ./x11vnc.service /usr/lib/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl start x11vnc
    sudo systemctl enable x11vnc
else
    sudo systemctl status x11vnc
fi







