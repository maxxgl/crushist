from django.shortcuts import get_object_or_404
from .models import Song, User, Event


def newUser():
    user = User.objects.create(user_name="guest")
    return user.pk


def queueSong(newSong, eventId):
    thumbnail = 'https://i.ytimg.com/vi/' + \
        newSong['yt_url'] + '/default.jpg'

    Song.objects.create(title=newSong['title'],
                        thumbnail_url=thumbnail,
                        yt_url=newSong['yt_url'],
                        event=get_object_or_404(Event, pk=eventId))


def vote(data):
    song = get_object_or_404(Song, pk=data['songId'])
    voter = get_object_or_404(User, pk=['userId'])
    if data['vote'] > 0:
        song.upvoters.add(voter)
    else:
        song.downvoters.add(voter)


def nextSong(eventId):
    event = get_object_or_404(Event, pk=eventId)
    songs = event.song_set.all()
    # newSong = songs.latest('votes')
    newSong = songs.latest()
    event.now_playing_id = newSong.yt_url
    event.save()
    event.now_playing_title = newSong.title
    event.save()
    newSong.delete()
    return {"title": event.now_playing_title, "videoId": event.now_playing_id}
