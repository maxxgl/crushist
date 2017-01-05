from django.shortcuts import render
from django.http import HttpResponse

from .models import Song


def home(request):

    # return response_with_context(context)
    return HttpResponse("<h1>Yeah we know it works - home")


def events(request, event_id):
    playlist = Song.objects.all()
    return HttpResponse("<h1>Yeah we know it works - event: %s" % event_id)


def users(request, user_id):

    return HttpResponse("<h1>Yeah we know it works - user: %s" % user_id)
