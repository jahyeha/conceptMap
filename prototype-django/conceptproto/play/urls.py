from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^videos/(?P<video_id>.+)/$', views.videos),
]
