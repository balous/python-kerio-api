import importlib
from pprint import pprint
from kerio.api.chainable_method import ChainableMethod
from kerio.api.session import Session

class Client(ChainableMethod, object):
    def __init__(self, **kwargs):
        self.session = Session(**kwargs)
        pass

    def __getattr__(self, name):
        return self.next_method(names = [name], session = self.session)
