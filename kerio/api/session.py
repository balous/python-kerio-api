from pprint import pprint
import urlparse
import random
import httplib
import json
import ssl
import kerio.api

class Session(object):
    def __init__(self, url, debug = False, insecure = False):

        self.url = urlparse.urlparse(url)

        self.debug = debug

        self.token = None
        self.cookie = None

        context = None

        if insecure:
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

        body = json.loads(resp.read())

        if self.debug:
            print('RESPONSE:')
            pprint(body)

        error = None
        if 'error' in body:
            error = body['error']

        if (resp.status != 200) or (error != None):
            raise kerio.api.Error(resp.status, error['message'])

        for h in resp.getheaders():
            if h[0] == 'set-cookie':
                self.cookie = h[1]

        return body['result']

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
            print('REQUEST:')
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

    def upload_file(self, data):

        boundary = '+----------ThIs_Is_tHe_bouNdaRY_$'

        headers = self.headers()
        headers['Accept'] = '*/*'
        headers['Content-Type'] = 'multipart/form-data; boundary=%s' % boundary

        lines = [
            '--' + boundary,
            'Content-Disposition: form-data; name="newFile.bin"; filename="newFile.bin"',
            'Content-Type: application/octet-stream',
            '',
            data,
            '--' + boundary + '--',
            '',
        ]

        body = '\r\n'.join(lines)

        url = self.url.path
        if url[:-1] != '/':
            url += '/'
        url += 'upload'

        self.session.request(
            'POST',
            url,
            body,
            headers
        )
        resp = self.session.getresponse()

        return self.process_json_response(resp)

    def download_file(self, path, chunk_size = 10240):
        headers = self.headers()
        headers['Accept'] = '*/*'

        self.session.request(
            'GET',
            path,
            "",
            headers
        )
        resp = self.session.getresponse()

        if resp.status != 200:
            raise kerio.api.Error(resp.status, None)

        data = resp.read(chunk_size)
        while len(data) != 0:
            yield data
            data = resp.read(chunk_size)
