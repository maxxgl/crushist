from channels import Channel, Group
from channels.sessions import channel_session
import json
from . import actions


def msg_consumer(message):
    data = json.loads(message['data'])
    re = Channel(message['reply'], channel_layer=message.channel_layer)

    if data['action'] == 'newUser':
        newUserId = actions.newUser()
        new_user_msg = json.dumps({
            "action": "newUser",
            "newUserId": newUserId,
        })
        re.send({"text": new_user_msg})

    elif data['action'] == 'vote':
        votedList = actions.vote(data)
        new_votes_msg = json.dumps({
            "action": "voted",
            "upvoted": votedList['upvoted'],
            "downvoted": votedList['downvoted'],
        })
        re.send({"text": new_votes_msg})

    elif data['action'] == 'queueSong':
        actions.queueSong(data, message['eventId'])

    elif data['action'] == 'nextSong':
        newSong = actions.nextSong(message['eventId'])
        new_song_msg = json.dumps({
            "action": "nextSong",
            "title": newSong['title'],
            "videoId": newSong['videoId']
        })
        re.send({"text": new_song_msg})

    refresh = json.dumps({"action": "refresh"})
    Group("event-%s" % message['eventId']).send({"text": refresh})


@channel_session
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    eventId = message.content['path'].strip("/")
    message.channel_session['eventId'] = eventId
    Group("event-%s" % eventId).add(message.reply_channel)
    connected = json.dumps({"action": "connected"})
    message.reply_channel.send({"text": connected})


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
