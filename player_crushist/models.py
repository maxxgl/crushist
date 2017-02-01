from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=25)

    def __str__(self):
        return self.user_name


class Event(models.Model):
    event_name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_code = models.CharField(max_length=6, unique=True)
    now_playing_id = models.CharField(max_length=25)
    now_playing_title = models.CharField(max_length=250)

    def __str__(self):
        return self.event_name


class Song(models.Model):
    title = models.CharField(max_length=250)
    thumbnail_url = models.URLField(max_length=200)
    yt_url = models.URLField(max_length=25)
    votes = models.IntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
