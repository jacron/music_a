from channels import route
from website.consumers import ws_disconnect, ws_message, ws_add

channel_routing = [
    route('websocket.connect', ws_add),
    route('websocket.disconnect', ws_disconnect),
    route("websocket.receive", ws_message),
    # route('http.request', 'website.consumers.http_consumer'),
]