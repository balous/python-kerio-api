import importlib
from pprint import pprint
from kerio.api.chainable_method import ChainableMethod
from kerio.api.session import Session

class Error(Exception):
    def __init__(self, code, error = None):
        self.code  = code
        self.error = error

        super(Error, self).__init__(self.format_message())

    def format_message(self):
        msg = "Http code: {}".format(self.code)

        if self.error != None:
                msg += ", json-rpc message: {}".format(self.error)

        return msg

class Client(ChainableMethod, object):
    def __init__(self, **kwargs):
        self.session = Session(**kwargs)

    def __getattr__(self, name):
        return self.next_method(names = [name], session = self.session)
