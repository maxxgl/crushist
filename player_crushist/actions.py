from django.shortcuts import get_object_or_404
from .models import Song, Event


def queueSong(newSong, eventId):
    thumbnail = 'https://i.ytimg.com/vi/' + \
        newSong['yt_url'] + '/default.jpg'

    Song.objects.create(title=newSong['title'],
                        thumbnail_url=thumbnail,
                        yt_url=newSong['yt_url'], votes=1,
                        event=get_object_or_404(Event, pk=eventId))


def vote(data):
    song = get_object_or_404(Song, pk=data['songId'])
    song.votes += int(data['vote'])
    song.save()


def nextSong(eventId):
    event = get_object_or_404(Event, pk=eventId)
    songs = event.song_set.all()
    newSong = songs.latest('votes')
    event.now_playing_id = newSong.id
    event.save()
    event.now_playing_title = newSong.title
    event.save()
    newSong.delete()
    return {"title": event.now_playing_title, "videoId": event.now_playing_id}
