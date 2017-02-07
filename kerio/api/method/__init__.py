from pprint import pprint
from kerio.api.chainable_method import ChainableMethod

class Generic(ChainableMethod, object):
    def __init__(self, **kwargs):
        self.names = kwargs['names']
        self.session = kwargs['session']

    def __getattr__(self, name):
        self.names.append(name)

        return self.next_method(names = self.names, session = self.session)

    def __call__(self, **params):
        method_name = '.'.join(self.names)
        return self.session.json_method(method_name, params)

class Upload(Generic):
    def __call__(self, path):

        with open(path, 'r') as file:
            return self.session.upload_file(file.read())

class Download(Generic):
    def __call__(self, path):

        return self.session.download_file(path)
