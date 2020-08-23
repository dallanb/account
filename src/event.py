from .services import Membership


def new_event_listener(event):
    topic = event.topic
    key = event.key
    data = event.value
    if topic == 'auth':
        Membership().handle_event(key=key, data=data)
