import xadmin
from xadmin import views

from experiments.models import Rack,Lab,LabModel,VMS,ReservationInfo


class RackAdmin(object):
    model_icon = 'fa fa-table'
    list_display = ['rack_name','rack_host','rack_port','rack_user','rack_pwd','rack_remark']
    search_fields = ['rack_name']
    list_filter = ['rack_name']
    list_per_page = 10


class LabModelAdmin(object):
    model_icon = 'fa fa-flask'
    list_display = ['lab_name', 'lab_tb']
    style_fields = {'lab_doc': 'ueditor'}
    list_per_page = 10

class LabAdmin(object):
    model_icon = 'fa fa-flask'
    list_display = ["lab_alias", 'lab_id','lab_gua_user','lab_rack_id' ]
    list_per_page = 10


class VMSAdmin(object):
    model_icon = 'fa fa-flask'
    list_display = ['vm_name', 'vm_snapshot', 'rack_id',"lab_id",'vm_remark']
    search_fields = ['vm_name','rack_id','lab_id']
    list_filter = ['vm_name','rack_id','lab_id']
    list_per_page = 10


class ReservationAdmin(object):
    model_icon = 'fa fa-flask'
    list_display = ['date', 'tb_id', 'user','rack',"lab"]
    list_per_page = 10





xadmin.site.register(Rack,RackAdmin)
xadmin.site.register(Lab,LabAdmin)
xadmin.site.register(LabModel,LabModelAdmin)
xadmin.site.register(VMS,VMSAdmin)
xadmin.site.register(ReservationInfo,ReservationAdmin)