from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Event


def home(request):

    # return response_with_context(context)
    return HttpResponse("<h1>Yeah we know it works - home")


def events(request, event_id):
    playlist = get_object_or_404(Event, pk=event_id)
    context = {'playlist': playlist}
    return render(request, 'player_crushist/events.html', context)


def users(request, user_id):

    return HttpResponse("<h1>Yeah we know it works - user: %s" % user_id)
