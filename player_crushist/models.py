import uuid
from django.db import models


class User(models.Model):
    id = models.CharField(primary_key=True, unique=True,
                          max_length=36, editable=False)
    user_name = models.CharField(max_length=20)

    def __str__(self):
        return self.user_name


class Event(models.Model):
    event_name = models.CharField(max_length=50)
    event_description = models.CharField(max_length=300, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_code = models.CharField(max_length=50, unique=True)
    now_playing_id = models.CharField(max_length=15, default="")
    now_playing_title = models.CharField(max_length=250, default="")
    now_playing_channel = models.CharField(max_length=250, default="")
    # now_playing_duration = models.CharField(max_length=250, default="")

    def __str__(self):
        return self.event_name


class Song(models.Model):
    title = models.CharField(max_length=120)
    yt_url = models.CharField(max_length=15)
    channel = models.CharField(max_length=25)
    # duration = models.CharField(max_length=10)
    added = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    upvoters = models.ManyToManyField(User, related_name="upvoters")
    downvoters = models.ManyToManyField(User, related_name="downvoters")
    votes = models.IntegerField(default=0)

    def updateVotes(self):
        self.votes = self.upvoters.all().count() - \
            self.downvoters.all().count()
        self.save()

    def __str__(self):
        return self.title
