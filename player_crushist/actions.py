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
    vote = data['vote']
    song = get_object_or_404(Song, pk=data['songId'])
    voter = get_object_or_404(User, pk=data['userId'])
    upvoted = song.upvoters.filter(id=voter.id).exists()
    downvoted = song.downvoters.filter(id=voter.id).exists()
    song.upvoters.remove(voter)
    song.downvoters.remove(voter)

    if vote > 0 and not upvoted:
        song.upvoters.add(voter)
    elif vote < 0 and not downvoted:
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
