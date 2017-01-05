from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<question_id>[0-9]+)/$', views.events, name='events'),
    url(r'^user/(?P<question_id>[0-9]+)/$', views.users, name='users'),
]
