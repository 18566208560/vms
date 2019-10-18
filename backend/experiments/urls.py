from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'experiment/$',views.Experiment.as_view()),
    url(r'getrack/$',views.GetRack.as_view()),
    url(r'getlab/(?P<rack_id>\d+)/$',views.GetLab.as_view()),
    url(r'reservation/(?P<rack_id>\d+)/(?P<lab_date>\d{4}\-\d{1,2}\-\d{1,2})/$',views.Reservation.as_view()),
    url(r'reservation/$',views.Reservation.as_view()),
    url(r'myreservations/(?P<userid>\d+)/$', views.MyReservation.as_view()),
    url(r'myreservations/$', views.MyReservation.as_view()),
    url(r'labdoc/$',views.GetLabDoc.as_view()),
    url(r'poweron/$',views.PowerOn.as_view()),
    url(r'snapshot/$',views.Snapshot.as_view()),
    url(r'vmstate/$',views.Vmstate.as_view()),
    ]
