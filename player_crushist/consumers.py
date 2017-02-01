from channels import Channel, Group
from channels.sessions import channel_session
import json
from . import actions


def msg_consumer(message):
    data = json.loads(message['data'])

    if data['action'] == 'vote':
        actions.vote(data)
    elif data['action'] == 'queueSong':
        actions.queueSong(data, message['eventId'])
    elif data['action'] == 'nextSong':
        newSong = actions.nextSong(message['eventId'])
        re = Channel(message['reply'], channel_layer=message.channel_layer)
        re.send({
            "action": "newSong",
            "title": json.dumps(newSong)
        })

    # Group("event-%s" % message['eventId']).send({"action": "refresh"})

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

    # reply_channel.send({
    #     "text": json.dumps(data),
    # })


@channel_session
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    eventId = message.content['path'].strip("/")
    message.channel_session['eventId'] = eventId
    Group("event-%s" % eventId).add(message.reply_channel)


@channel_session
def ws_message(message):
    Channel("event-messages").send({
        "eventId": message.channel_session['eventId'],
        "data": message['text'],
        "reply": message['reply_channel']
    })


@channel_session
def ws_disconnect(message):
    Group("event-%s" % message.channel_session['eventId']).discard(
        message.reply_channel)
