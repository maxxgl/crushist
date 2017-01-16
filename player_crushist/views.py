from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Event


def home(request):
    context = {}
    return render(request, 'player_crushist/master.html', context)

    
def events(request, event_id):
    playlist = get_object_or_404(Event, pk=event_id)
    context = {'playlist': playlist}
    return render(request, 'player_crushist/events.html', context)


def users(request, user_id):
    return HttpResponse("<h1>Yeah we know it works - user: %s" % user_id)


def new_event(request):
    return HttpResponse("<h1>Yeah we know it works - new event")


def new_user(request):
    return HttpResponse("<h1>Yeah we know it works - new user")
