from channels import Channel, Group
from channels.sessions import channel_session
import json
from . import actions


def msg_consumer(message):
    data = json.loads(message['data'])
    re = Channel(message['reply'], channel_layer=message.channel_layer)

    if data['action'] == 'newUser':
        new_user_msg = json.dumps({
            "action": "newUser",
            "newUserId": actions.newUser(),
        })
        re.send({"text": new_user_msg})

    elif data['action'] == 'vote':
        msg = {"action": "voted"}
        msg.update(actions.vote(data))
        re.send({"text": json.dups(msg)})

    elif data['action'] == 'queueSong':
        if actions.queueSong(data, message['eventId']) == 1:
            oneQueued = json.dumps({"action": "oneQueued"})
            Group("event-%s" % message['eventId']).send({"text": oneQueued})

    elif data['action'] == 'nextSong':
        msg = {"action": "nextSong"}
        msg.update(actions.nextSong(message['eventId']))
        Group("event-%s" % message['eventId']).send({"text": json.dumps(msg)})

    refresh = json.dumps({"action": "refresh"})
    Group("event-%s" % message['eventId']).send({"text": refresh})


@channel_session
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    eventId = message.content['path'].strip("/")
    connected = {"action": "connected"}
    message.channel_session['eventId'] = eventId
    Group("event-%s" % eventId).add(message.reply_channel)
    if eventId != "create":
        connected.update(actions.np(eventId))
    message.reply_channel.send({"text": json.dumps(connected)})


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
