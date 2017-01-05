from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^/events/(?P<question_id>[0-9]+)/$', views.events, name='events'),
    url(r'^/users/(?P<question_id>[0-9]+)/$', views.users, name='users'),
]
