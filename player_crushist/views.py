from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Event, User


def home(request):
    context = {}
    return render(request, 'player_crushist/home.html', context)


def events(request, event_id):
    playlist = get_object_or_404(Event, pk=event_id)
    context = {'playlist': playlist}
    return render(request, 'player_crushist/events.html', context)


def playlist(request, event_id):
    playlist = get_object_or_404(Event, pk=event_id)
    context = {'playlist': playlist}
    return render(request, 'player_crushist/partials/playlist.html', context)


def users(request, user_id):
    return HttpResponse("<h1>Yeah we know it works - user: %s" % user_id)


def newEvent(request):
    context = {}
    return render(request, 'player_crushist/newEvent.html', context)


def eventCreator(request):
    event = Event.objects.create(
        event_name=request.POST['event_name'],
        user=get_object_or_404(User, pk=request.POST['user_id']),
        event_code=request.POST['event_code']
    )
    return HttpResponseRedirect(
        reverse('player_crushist:events', args=(event.id,)))


def newUser(request):
    return HttpResponse("<h1>Yeah we know it works - new user")
