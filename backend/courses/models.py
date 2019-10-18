from django.db import models
import datetime
# Create your models here.

class TeacherInfo(models.Model):
    teacher = models.CharField(verbose_name='授课老师', max_length=10)

    class Meta:
        db_table = 'tb_teacher'
        verbose_name = '教师表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.teacher

class CourseDate(models.Model):
    OPENDATE_CHOICE = (
        (1,'否'),
        (2,'是')
    )
    date = models.DateField(verbose_name='上课日期')
    opendate = models.SmallIntegerField(choices=OPENDATE_CHOICE,verbose_name='是否为开课日期',default=1)

    class Meta:
        db_table = 'tb_coursedate'
        verbose_name = '课程日期表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return datetime.datetime.strftime(self.date,'%Y-%m-%d')

class CourseSchedule(models.Model):
    COURSE_CHOICE = (
        (1,'HCIA-RS'),
        (2,'HCIP-RS'),
        (3,'HCIE-RS'),
        (4,'HCIA-CLOUD'),
        (5,'HCIP-CLOUD'),
        (6,'HCIE-CLOUD'),
        (7,'华为云计算融合班'),
        (8,'其他')
    )
    COURSETYPE_CHOICE = (
        (1, '周末班'),
        (2, '脱产班'),
        (3, '暑假班'),
        (4, '融合班'),
        (5, '嵌入式'),
        (6, '实训'),
        (7, '其他')
    )

    school = models.CharField(verbose_name='学校名称',max_length=30)
    course = models.SmallIntegerField(choices=COURSE_CHOICE,verbose_name='课程名称')
    coursetype = models.SmallIntegerField(choices=COURSETYPE_CHOICE,verbose_name='课程类型')
    classroom = models.CharField(verbose_name='课室',max_length=10)
    schooltime = models.CharField(verbose_name='上课时间',max_length=40)
    comment = models.CharField(verbose_name='备注',max_length=60,blank=True)
    teacher = models.ForeignKey(TeacherInfo,verbose_name='授课老师',on_delete=models.CASCADE)
    coursedate = models.ForeignKey(CourseDate,verbose_name='上课日期',on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_couserse'
        verbose_name = '课程安排表'
        verbose_name_plural = verbose_name



