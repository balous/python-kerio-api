from pprint import pprint
import urlparse
import random
import httplib
import json
import ssl
import kerio.api

class Session(object):
    def __init__(self, **params):

        self.url = urlparse.urlparse(params['url'])

        self.debug = params['debug']

        self.token = None
        self.cookie = None

        context = None

        if params['insecure']:
            context = ssl._create_unverified_context()

        self.session = httplib.HTTPSConnection(
            host = self.url.hostname,
            port = self.url.port,
            context = context
        )

    def set_token(self, token):
        self.token = token

    def headers(self):
        h = {}
        if not self.token == None:
            h['X-Token'] = self.token

        if not self.cookie == None:
            h['Cookie'] = self.cookie

        return h

    def process_json_response(self, resp):

        if resp.status != 200:
            raise kerio.api.Error(resp)

        for h in resp.getheaders():
            if h[0] == 'set-cookie':
                self.cookie = h[1]

        body = json.loads(resp.read())

        if self.debug:
            pprint(body)

        if 'error' in body:
            raise kerio.api.Error(body)

        return body

    def json_method(self, name, params):

        body = {
            'jsonrpc': '2.0',
            'id': random.randint(100000, 900000),
            'method': name,
            'params': params,
        }
        if self.token != None:
            body['token'] = self.token

        if self.debug:
            pprint(body)

        headers = self.headers()
        headers['Accept'] = 'application/json-rpc'

        self.session.request(
            'POST',
            self.url.path,
            json.dumps(body),
            headers
        )
        resp = self.session.getresponse()

        return self.process_json_response(resp)
