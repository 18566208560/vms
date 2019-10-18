import xadmin
from xadmin import views

from . import models


class InterviewAdmin(object):
    model_icon = 'fa fa-table'
    list_display = ['date','tb_id','num','comment','user']
    search_fields = ['date']
    list_filter = ['date']
    list_per_page = 10



xadmin.site.register(models.InterviewInfo,InterviewAdmin)