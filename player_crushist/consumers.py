from channels import Channel, Group
from channels.sessions import channel_session
import json
from . import actions
import sys


def msg_consumer(message):
    data = json.loads(message['data'])

    if data['action'] == 'vote':
        actions.vote(data)
    elif data['action'] == 'queueSong':
        actions.queueSong()

    # reply_channel = Channel(
    #     message['reply'],
    #     channel_layer=message.channel_layer,
    # )

    # data = {
    #     "action": "voted",
    #     "songId": song.pk,
    #     "vote": "up" if message['vote'] > 0 else "down",
    # }
    # groupData = {
    #     "action": "newVote",
    #     "songId": song.pk,
    #     "votes": song.votes,
    # }

    # Group("event-%s" % message['eventId']).send({
    #     "text": json.dumps(groupData),
    # })
    # reply_channel.send({
    #     "text": json.dumps(data),
    # })


@channel_session
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    eventId = message.content['path'].strip("/event/")
    message.channel_session['eventId'] = eventId
    Group("event-%s" % eventId).add(message.reply_channel)


@channel_session
def ws_message(message):
    print(message['text'], file=sys.stderr)
    Channel("event-messages").send({
        "eventId": message.channel_session['eventId'],
        "data": message['text'],
        "reply": message['reply_channel']
    })


@channel_session
def ws_disconnect(message):
    Group("event-%s" % message.channel_session['eventId']).discard(
        message.reply_channel)
