
import csv
import hashlib


sql = 'insert into tb_userinfo (username,password,email,realname,phone,qq,adress) values("%s","%s","%s","%s","%s","%s","%s");'

with open("d:/project/yeslab-booking-systerm/docker_compose/data.csv","r", encoding="utf-8")as f,open("d:/project/yeslab-booking-systerm/docker_compose/user.sql","w",encoding="utf-8")as f1:
    reader = csv.reader(f)
    for row in reader:
        passwd = hashlib.sha224(row[6].encode()).hexdigest()
        sqls = sql%(row[1],passwd,row[7],row[2],row[3],row[4],row[5])
        f1.writelines(sqls)

        