#! /home/python/.virtualenvs/meiduo_django/bin/python3
# -*-coding:utf-8-*-

import sys
sys.path.insert(0,'../')

import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'bookingSysterm.settings'

# 让ｄｊａｎｇｏ进行初始化设置
import django
django.setup()

from infos.models import ReservationInfo
import datetime

def main():
    today = datetime.date.today()

    t = today + datetime.timedelta(days=6)

    for j in range(1,17):
        reser = ReservationInfo(date=t,tb_id=j)
        reser.save()

if __name__ == '__main__':
    main()