import xadmin
from xadmin import views
from django.contrib import admin

from . import models

class CourseAdmin(object):
    # 显示的列
    list_display = ['teacher','school', 'course','coursetype','coursedate','schooltime','classroom']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['teacher', 'school', 'course', 'coursetype','coursedate']
    # # 过滤
    list_filter = [ 'teacher','school', 'course', 'coursetype','coursedate']
xadmin.site.register(models.CourseSchedule,CourseAdmin)

class CourseStackInline(object):
    # 创建一个可被coursedate关联的对象，通过上课日期可编辑course表
    """类型InlineModelAdmin：表示在模型的编辑页面嵌入关联模型的编辑。
    子类TabularInline：以表格的形式嵌入。
    子类StackedInline：以块的形式嵌入。"""
    model = models.CourseSchedule
    extra = 3
class CourseDateAdmin(object):
    list_display = ['id','date']
    inlines = [CourseStackInline]
    model_icon = 'fa fa-book'

xadmin.site.register(models.CourseDate,CourseDateAdmin)

