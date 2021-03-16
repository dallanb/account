import logging

from src.events import Auth


def new_event_listener(event):
    topic = event.topic
    key = event.key
    data = event.value
    if topic == 'auth_test':
        try:
            Auth().handle_event(key=key, data=data)
        except Exception as ex:
            logging.error(ex)
            logging.info('Auth event err')
