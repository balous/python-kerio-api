from pprint import pprint

class Session(object):
    def __init__(self, **params):
        self.params = params

    def json_method(self, name, params):
        pprint(name)
        pprint(params)
