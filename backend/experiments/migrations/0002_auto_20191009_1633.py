# Generated by Django 2.1.4 on 2019-10-09 08:33

import DjangoUeditor.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_userinfo'),
        ('experiments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab_alias', models.CharField(max_length=100, verbose_name='实验别名')),
                ('lab_gua_user', models.CharField(max_length=100, verbose_name='guacamole用户名')),
                ('lab_remark', models.CharField(max_length=300, verbose_name='lab 备注')),
            ],
            options={
                'verbose_name': 'lab实验表',
                'verbose_name_plural': 'lab实验表',
            },
        ),
        migrations.CreateModel(
            name='LabModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab_name', models.CharField(max_length=100, verbose_name='lab名称')),
                ('lab_tb', models.CharField(max_length=500, verbose_name='lab时间段')),
                ('lab_doc', DjangoUeditor.models.UEditorField(verbose_name='lab文档')),
            ],
            options={
                'verbose_name': 'lab实验模型',
                'verbose_name_plural': 'lab实验模型',
            },
        ),
        migrations.CreateModel(
            name='Rack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rack_name', models.CharField(max_length=100, verbose_name='Rock名称')),
                ('rack_host', models.CharField(max_length=100, verbose_name='Rock host')),
                ('rack_port', models.CharField(max_length=100, verbose_name='Rock port')),
                ('rack_user', models.CharField(max_length=100, verbose_name='Rock user')),
                ('rack_pwd', models.CharField(max_length=100, verbose_name='Rock pwd')),
                ('rack_remark', models.CharField(max_length=300, verbose_name='Rock 备注')),
                ('rack_show', models.SmallIntegerField(default=1, verbose_name='是否显示')),
            ],
            options={
                'verbose_name': 'rack表',
                'verbose_name_plural': 'rack表',
            },
        ),
        migrations.CreateModel(
            name='ReservationInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='预约日期')),
                ('tb_id', models.CharField(max_length=20, verbose_name='预约时段')),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='experiments.Lab', verbose_name='labid')),
                ('rack', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='experiments.Rack', verbose_name='rackid')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.UserInfo', verbose_name='用户名')),
            ],
            options={
                'verbose_name': '实验预约信息表',
                'verbose_name_plural': '实验预约信息表',
            },
        ),
        migrations.CreateModel(
            name='VMS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vm_name', models.CharField(max_length=100, verbose_name='虚拟机名称')),
                ('vm_id', models.CharField(max_length=100, verbose_name='虚拟机id')),
                ('vm_snapshot', models.CharField(max_length=100, verbose_name='虚拟机快照')),
                ('vm_snapshot_id', models.CharField(max_length=100, verbose_name='虚拟机快照id')),
                ('vm_remark', models.CharField(max_length=300, verbose_name='备注')),
                ('lab_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='experiments.Lab', verbose_name='labid')),
                ('rack_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='experiments.Rack', verbose_name='rackid')),
            ],
            options={
                'verbose_name': '虚拟机列表',
                'verbose_name_plural': '虚拟机列表',
            },
        ),
        migrations.AddField(
            model_name='lab',
            name='lab_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='lab_m', to='experiments.LabModel', verbose_name='实验模型'),
        ),
        migrations.AddField(
            model_name='lab',
            name='lab_rack_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='r_rack', to='experiments.Rack', verbose_name='rackid'),
        ),
    ]
