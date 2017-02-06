import importlib
from pprint import pprint
from kerio.api.chainable_method import ChainableMethod
from kerio.api.session import Session

class Error(Exception):
    def __init__(self, resp):
        self.resp = resp

        super(Error, self).__init__(resp['error']['message'])

class Client(ChainableMethod, object):
    def __init__(self, **kwargs):
        self.session = Session(**kwargs)

    def __getattr__(self, name):
        return self.next_method(names = [name], session = self.session)
