from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    # url(r'^video/(?P<submitted_video_id>.+)/$', views.video),
    url(r'^video/$', views.video),
]
