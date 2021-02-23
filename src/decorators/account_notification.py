from functools import wraps

from src.notifications import account_active, account_pending, account_inactive


class account_notification:
    def __init__(self, operation):
        self.operation = operation

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            prev_instance = {**kwargs.get('instance').__dict__} if kwargs.get('instance') else None
            new_instance = f(*args, **kwargs)

            if self.operation == 'create':
                self.create(new_instance=new_instance)
            if self.operation == 'update':
                self.update(prev_instance=prev_instance, new_instance=new_instance)

            return new_instance

        wrap.__doc__ = f.__doc__
        wrap.__name__ = f.__name__
        return wrap

    @staticmethod
    def create(new_instance):
        if new_instance.status.name == 'active':
            account_active.from_data(account=new_instance).notify()
        if new_instance.status.name == 'inactive':
            account_inactive.from_data(account=new_instance).notify()
        if new_instance.status.name == 'pending':
            account_pending.from_data(account=new_instance).notify()

    @staticmethod
    def update(prev_instance, new_instance):
        if prev_instance and prev_instance.get('status') and prev_instance['status'].name != new_instance.status.name:
            if new_instance.status.name == 'active':
                account_active.from_data(account=new_instance).notify()
            if new_instance.status.name == 'inactive':
                account_inactive.from_data(account=new_instance).notify()
            if new_instance.status.name == 'pending':
                account_pending.from_data(account=new_instance).notify()
