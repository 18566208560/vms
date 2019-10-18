# Generated by Django 2.1.4 on 2019-10-09 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='上课日期')),
                ('opendate', models.SmallIntegerField(choices=[(1, '否'), (2, '是')], default=1, verbose_name='是否为开课日期')),
            ],
            options={
                'verbose_name': '课程日期表',
                'verbose_name_plural': '课程日期表',
                'db_table': 'tb_coursedate',
            },
        ),
        migrations.CreateModel(
            name='CourseSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(max_length=30, verbose_name='学校名称')),
                ('course', models.SmallIntegerField(choices=[(1, 'HCIA-RS'), (2, 'HCIP-RS'), (3, 'HCIE-RS'), (4, 'HCIA-CLOUD'), (5, 'HCIP-CLOUD'), (6, 'HCIE-CLOUD'), (7, '华为云计算融合班'), (8, '其他')], verbose_name='课程名称')),
                ('coursetype', models.SmallIntegerField(choices=[(1, '周末班'), (2, '脱产班'), (3, '暑假班'), (4, '融合班'), (5, '嵌入式'), (6, '实训'), (7, '其他')], verbose_name='课程类型')),
                ('classroom', models.CharField(max_length=10, verbose_name='课室')),
                ('schooltime', models.CharField(max_length=40, verbose_name='上课时间')),
                ('comment', models.CharField(blank=True, max_length=60, verbose_name='备注')),
                ('coursedate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.CourseDate', verbose_name='上课日期')),
            ],
            options={
                'verbose_name': '课程安排表',
                'verbose_name_plural': '课程安排表',
                'db_table': 'tb_couserse',
            },
        ),
        migrations.CreateModel(
            name='TeacherInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher', models.CharField(max_length=10, verbose_name='授课老师')),
            ],
            options={
                'verbose_name': '教师表',
                'verbose_name_plural': '教师表',
                'db_table': 'tb_teacher',
            },
        ),
        migrations.AddField(
            model_name='courseschedule',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.TeacherInfo', verbose_name='授课老师'),
        ),
    ]
