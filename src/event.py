from .services import Account


def new_event_listener(event):
    topic = event.topic
    key = event.key
    data = event.value
    if topic == 'auth':
        Account().handle_event(key=key, data=data)
