from functools import wraps


class account_notification:
    def __init__(self, operation):
        self.operation = operation
        self.topic = 'accounts'
        self._service = None

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            self.service = args[0]
            prev_instance = {**kwargs.get('instance').__dict__} if kwargs.get('instance') else None
            new_instance = f(*args, **kwargs)

            if self.operation == 'create':
                self.create(new_instance=new_instance)
            if self.operation == 'update':
                self.update(prev_instance=prev_instance, new_instance=new_instance, args=kwargs)

            return new_instance

        wrap.__doc__ = f.__doc__
        wrap.__name__ = f.__name__
        return wrap

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, service):
        self._service = service

    def create(self, new_instance):
        key = 'account_created'
        value = {'uuid': str(new_instance.uuid), 'user_uuid': str(new_instance.user_uuid), 'email': new_instance.email,
                 'username': new_instance.username, 'display_name': new_instance.display_name}
        self.service.notify(topic=self.topic, value=value, key=key, )

    def update(self, prev_instance, new_instance, args):
        key = 'account_updated'
        value = {'uuid': str(new_instance.uuid)}
        self.service.notify(topic=self.topic, value=value, key=key, )
