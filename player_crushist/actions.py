from django.shortcuts import get_object_or_404
from .models import Song, User, Event


def newUser():
    user = User.objects.create(user_name="guest")
    return user.pk


def queueSong(newSong, code):
    thumbnail = 'https://i.ytimg.com/vi/' + \
        newSong['yt_url'] + '/mqdefault.jpg'

    Song.objects.create(title=newSong['title'],
                        thumbnail_url=thumbnail,
                        yt_url=newSong['yt_url'],
                        event=get_object_or_404(Event, event_code=code))


def vote(data):
    user = get_object_or_404(User, pk=data['userId'])
    if data['songId'] is not 0:
        vote = data['vote']
        song = get_object_or_404(Song, pk=data['songId'])
        upvoted = song.upvoters.filter(id=user.id).exists()
        downvoted = song.downvoters.filter(id=user.id).exists()
        song.upvoters.remove(user)
        song.downvoters.remove(user)

        if vote > 0 and not upvoted:
            song.upvoters.add(user)
        elif vote < 0 and not downvoted:
            song.downvoters.add(user)

        song.updateVotes()

    uplist = []
    downlist = []
    for i in Song.objects.filter(upvoters=user).values_list('id', flat=True):
        uplist.append(i)
    for i in Song.objects.filter(downvoters=user).values_list('id', flat=True):
        downlist.append(i)

    return {
        "upvoted": uplist,
        "downvoted": downlist
    }


def nextSong(code):
    event = get_object_or_404(Event, event_code=code)
    songs = event.song_set.all()
    newSong = songs.latest('votes')
    event.now_playing_id = newSong.yt_url
    event.save()
    event.now_playing_title = newSong.title
    event.save()
    newSong.delete()
    return {"title": event.now_playing_title, "videoId": event.now_playing_id}
