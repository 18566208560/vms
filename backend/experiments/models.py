from django.db import models
from users.models import UserInfo
from DjangoUeditor.models import UEditorField
import datetime
# Create your models here.

class Rack(models.Model):
    """rack表"""
    rack_name = models.CharField(max_length=100,verbose_name='Rock名称')
    rack_host = models.CharField(max_length=100,verbose_name='Rock host')
    rack_port = models.CharField(max_length=100,verbose_name='Rock port')
    rack_user = models.CharField(max_length=100,verbose_name='Rock user')
    rack_pwd = models.CharField(max_length=100,verbose_name='Rock pwd')
    rack_remark = models.CharField(max_length=300,verbose_name='Rock 备注')
    rack_show = models.SmallIntegerField(default=1,verbose_name="是否显示")
    class Meta:
        verbose_name = "rack表"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.rack_name

class LabModel(models.Model):
    lab_name = models.CharField(max_length=100, verbose_name='lab名称')
    lab_tb = models.CharField(max_length=500,verbose_name="lab时间段")  # {"1":"00:00-6:00","2":"6:30-10:30","3":"11:00-15:00","4":"15:30-19:30","5":"20:00-23:59",} 不能写24：00
    lab_doc = UEditorField(width=1000, height=300,toolbars="full",verbose_name="lab文档")

    class Meta:
        verbose_name = "lab实验模型"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.lab_name


class Lab(models.Model):
    """"lab实验表"""
    lab_id = models.ForeignKey(LabModel,on_delete=models.DO_NOTHING,related_name="lab_m",verbose_name="实验模型")
    lab_alias = models.CharField(max_length=100,verbose_name="实验别名")
    lab_gua_user = models.CharField(max_length=100,verbose_name="guacamole用户名")
    lab_rack_id = models.ForeignKey(Rack,on_delete=models.DO_NOTHING,related_name="r_rack",verbose_name="rackid")
    lab_remark = models.CharField(max_length=300, verbose_name='lab 备注')
    class Meta:
        verbose_name = "lab实验表"
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.lab_alias


#
class VMS(models.Model):
    """虚拟机列表"""
    vm_name = models.CharField(max_length=100,verbose_name="虚拟机名称")
    vm_id = models.CharField(max_length=100,verbose_name="虚拟机id")
    vm_snapshot = models.CharField(max_length=100,verbose_name="虚拟机快照")
    vm_snapshot_id = models.CharField(max_length=100,verbose_name="虚拟机快照id")
    rack_id = models.ForeignKey(Rack,on_delete=models.DO_NOTHING,verbose_name="rackid")
    lab_id = models.ForeignKey(Lab,on_delete=models.DO_NOTHING,verbose_name="labid")
    vm_remark = models.CharField(max_length=300,verbose_name="备注")

    class Meta:
        verbose_name = "虚拟机列表"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.vm_name

class ReservationInfo(models.Model):
    date = models.DateField(verbose_name='预约日期')
    tb_id = models.CharField(max_length=20,verbose_name='预约时段')
    rack = models.ForeignKey(Rack,on_delete=models.DO_NOTHING,verbose_name="rackid")
    lab = models.ForeignKey(Lab,on_delete=models.DO_NOTHING,verbose_name="labid")
    user = models.ForeignKey(UserInfo,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="用户名")

    class Meta:
        verbose_name = '实验预约信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return datetime.datetime.strftime(self.date,'%Y-%m-%d')