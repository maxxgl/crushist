from django.conf.urls import url

from . import views


app_name = 'player_crushist'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<event_id>[0-9]+)/$', views.events, name='events'),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.users, name='users'),
    url(r'^(?P<event_id>[0-9]+)/playlist/$', views.playlist, name='playlist'),
    url(r'^create/$', views.newEvent, name='newEvent')
]
