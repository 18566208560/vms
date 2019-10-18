from django.conf.urls import url
from . import views
from django.views.decorators.csrf import csrf_exempt
# from rest_framework_jwt.views import obtain_jwt_token
# from rest_framework_jwt.views import refresh_jwt_token
# from rest_framework_jwt.views import verify_jwt_token
urlpatterns = [
    url(r'captcha/(?P<uuid>.+)/$',views.Captcha.as_view()),
    url(r'register/',csrf_exempt(views.Register.as_view())),
    url(r'login/',csrf_exempt(views.Login.as_view())),
    url(r'email/(?P<uuid>[a-z0-9-]{36})/(?P<email>[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+)/$', views.Forgot.as_view()),
    url(r'forgot/$', views.Forgot.as_view()),
    url(r'userinfo/(?P<user_id>\d+)$',views.UserInfos.as_view()),
    # url(r'^api-token-auth/', obtain_jwt_token),
    # url(r'^api-token-refresh/', refresh_jwt_token),
    # url(r'^api-token-verify/', verify_jwt_token)

]
