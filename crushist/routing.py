from channels.routing import route
from player_crushist.consumers import ws_connect, \
    ws_message, ws_disconnect, msg_consumer

channel_routing = [
    route("event-messages", msg_consumer),
    route("websocket.connect", ws_connect),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]
