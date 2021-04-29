import logging
from functools import wraps

from src.notifications import country_updated


class address_notification:
    def __init__(self, operation):
        self.operation = operation

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            prev_instance = {**kwargs.get('instance').__dict__} if kwargs.get('instance') else None
            new_instance = f(*args, **kwargs)

            if self.operation == 'update':
                self.update(prev_instance=prev_instance, new_instance=new_instance)

            return new_instance

        wrap.__doc__ = f.__doc__
        wrap.__name__ = f.__name__
        return wrap

    @staticmethod
    def update(prev_instance, new_instance):
        if prev_instance and prev_instance.get('country') and prev_instance['country'].code != new_instance.country:
            country_updated.from_data(address=new_instance).notify()
