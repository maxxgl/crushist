from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=25)

    def __str__(self):
        return self.user_name


class Event(models.Model):
    event_name = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.event_name


class Song(models.Model):
    title = models.CharField(max_length=250)
    yt_url = models.URLField(max_length=500)
    votes = models.IntegerField(default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
