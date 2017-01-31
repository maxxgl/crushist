from django.shortcuts import get_object_or_404
from .models import Song, Event


def queueSong(data):
    Song.objects.create(title=data['title'], thumbnail_url=data['thumbnail'],
                        yt_url=data['yt_url'], votes=1,
                        event=get_object_or_404(Event, pk=data['eventId']))


def vote(data):
    song = get_object_or_404(Song, pk=data['songId'])
    song.votes += int(data['vote'])
    song.save()
