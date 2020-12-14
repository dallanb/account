from .events import *


def new_event_listener(event):
    topic = event.topic
    key = event.key
    data = event.value
    if topic == 'auth':
        Auth().handle_event(key=key, data=data)
