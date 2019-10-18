import xadmin
from xadmin import views
from . import models

class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "yeslab预约系统后台管理"  # 设置站点标题
    site_footer = "广州京睿科技有限公司"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠





class UserInfoAdmin(object):
    model_icon = 'fa fa-table'
    list_display = ['username','realname','email','phone','qq','adress']
    search_fields = ['username','realname','email','phone','qq','adress']
    list_filter = ['adress']
    list_per_page = 10


xadmin.site.register(models.UserInfo,UserInfoAdmin)

xadmin.site.register(views.CommAdminView, GlobalSettings)