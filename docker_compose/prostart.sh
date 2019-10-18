#!/bin/sh
sudo cp ../backend/requirements.txt ./python/
# 软链接 目录 注意 第一个为源目录（最好为绝对路径，若为相对路径，是相对后一个目录的）
sudo ln -s ../../backend/static ./nginx/static
sudo ln -s ../../frontend ./nginx/html
