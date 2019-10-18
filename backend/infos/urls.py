from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'myinterview/$',views.MyInterview.as_view()),
    url(r'interview_msg/$',views.Interview.as_view()),
    url(r'interview/$',views.Interview.as_view()),

    ]