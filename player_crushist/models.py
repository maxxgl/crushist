from django.db import models


class Song(models.Model):
    song_title = models.CharField(max_length=250)
    song_url = models.URLField(max_length=500)
    song_votes = models.IntegerField(default=0)


class Event(models.Model):
    event_name = models.CharField(max_length=250)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)


class User(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=25)
