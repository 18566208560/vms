# Generated by Django 2.1.4 on 2019-10-09 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=12, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=12, verbose_name='密码')),
                ('realname', models.CharField(default='', max_length=20, verbose_name='真实姓名')),
                ('email', models.CharField(default='', max_length=50, verbose_name='邮箱')),
                ('phone', models.CharField(default='', max_length=11, verbose_name='手机号')),
                ('qq', models.CharField(default='', max_length=11, verbose_name='QQ')),
                ('adress', models.CharField(default='', max_length=30, verbose_name='学校/企业名称')),
            ],
            options={
                'verbose_name': '用户信息表',
                'verbose_name_plural': '用户信息表',
                'db_table': 'tb_userinfo',
            },
        ),
    ]
