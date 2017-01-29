from channels import Channel, Group
from channels.sessions import channel_session
from django.shortcuts import get_object_or_404
from .models import Song
import json


def actions_consumer():
    song = get_object_or_404(Song, pk=1)
    data = {
        "action": "newVote",
        "songId": "1",
        "vote": song.votes,
    }
    Group("event-1").send({
        "text": json.dumps(data),
    })

def msg_consumer(message):
    song = get_object_or_404(Song, pk=message.content['songId'])
    song.votes += int(message.content['vote'])
    song.save()
    reply_channel = Channel(
        message['reply'],
        channel_layer=message.channel_layer,
    )

    data = {
        "action": "voted",
        "songId": song.pk,
        "vote": "up" if message['vote'] > 0 else "down",
    }
    reply_channel.send({
        "text": json.dumps(data),
    })


@channel_session
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    eventId = message.content['path'].strip("/event/")
    message.channel_session['eventId'] = eventId
    Group("event-%s" % eventId).add(message.reply_channel)


@channel_session
def ws_message(message):
    data = json.loads(message['text'])
    Channel("event-messages").send({
        "eventId": message.channel_session['eventId'],
        "songId": data['songId'],
        "vote": data['vote'],
        "reply": message['reply_channel']
    })


@channel_session
def ws_disconnect(message):
    Group("event-%s" % message.channel_session['eventId']).discard(
        message.reply_channel)
