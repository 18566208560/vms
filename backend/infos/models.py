import datetime
from django.db import models
from users.models import UserInfo
from experiments.models import Rack,Lab
from utils.constant import TIME_BUKET


# Create your models here.


# class PeriodInfo(models.Model):
#     PERIOD_CHOICES = tuple(TIME_BUKET.items())
#     period = models.SmallIntegerField(choices=PERIOD_CHOICES,verbose_name='预约时段')
#     # 级联，删除主表(tb_reservationinfo)数据时连同一起删除外键表中的数据
#     reservation = models.ForeignKey(ReservationInfo,on_delete=models.CASCADE)
#     # 设置为NULL，仅在该字段null=True允许为null时可用
#     user = models.ForeignKey(UserInfo,on_delete=models.SET_NULL,null=True,blank=True)
#     class Meta:
#         db_table = 'tb_period'
#         verbose_name = '预约时段表'
#         verbose_name_plural = verbose_name

class InterviewInfo(models.Model):
    PERIOD_CHOICES = (
        (1, '上午'),
        (2, '下午'),
        (3,'晚上')
    )
    date = models.DateField(verbose_name='开放预约日期')
    tb_id = models.SmallIntegerField(choices=PERIOD_CHOICES,verbose_name='开放面试时段')
    num = models.SmallIntegerField(default=6,verbose_name='可预约人数')
    comment = models.CharField(verbose_name='备注说明(选填)',max_length=50,blank=True,default='')
    user = models.ManyToManyField(UserInfo,null=True,blank=True,verbose_name='预约学生(选填)')

    class Meta:
        db_table = 'interview'
        verbose_name = '面试预约信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.date,'上午' if self.tb_id ==1 else '下午')

