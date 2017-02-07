import kerio.api.method
from pprint import pprint

class Login(kerio.api.method.Generic):

    def __call__(self, **params):
        resp = super(Login, self).__call__(**params)

        token = resp['token']

        self.session.set_token(token)

        return resp
