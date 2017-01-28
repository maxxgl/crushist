from channels import Channel, Group
from channels.sessions import channel_session
from .models import Song


def msg_consumer(message):
    print("msg consumed")
    # Song.objects.create(
    #     event=message.content['event'],
    #     message=message.content['message'],
    # )
    Group("event-%s" % message.content['eventId']).send({
        "text": message.content['text'],
    })


@channel_session
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    eventId = message.content['path'].strip("/event/")
    message.channel_session['eventId'] = eventId
    Group("event-%s" % eventId).add(message.reply_channel)


@channel_session
def ws_message(message):
    print("msg recieved - '%s'" % message['text'])
    Channel("event-messages").send({
        "eventId": message.channel_session['eventId'],
        "text": message['text'],
    })


@channel_session
def ws_disconnect(message):
    Group("event-%s" % message.channel_session['eventId']).discard(
        message.reply_channel)
