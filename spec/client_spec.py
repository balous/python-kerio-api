import sys
import httpretty
from expects import *
from mock import MagicMock, patch, mock_open
import kerio.api
from pprint import pprint
import json
import ssl
import random

with description(kerio.api.Client):

    httpretty.HTTPretty.allow_net_connect = False
    httpretty.enable()

    random.randint = MagicMock(return_value = 1)

    with before.each:
        # standard response used by most testcases
        httpretty.register_uri(
            httpretty.POST,
            'https://1.1.1.1/api',
            body = json.dumps(
                {
                    "result": ':-)',
                    "jsonrpc": "2.0",
                    "id": 1,
                }
            ),
        )

    with description('__init__'):
        with context('default params'):
            with it('calls the method'):
                with \
                    patch('ssl._create_unverified_context'), \
                    patch('kerio.api.session.pprint'), \
                    patch('sys.stdout') as stdout:

                    c = kerio.api.Client(url = 'https://1.1.1.1/api')

                    c.request(a = '1', b = '2')

                    expect(kerio.api.session.pprint.call_count).to(be(0))
                    expect(sys.stdout.write.call_count).to(be(0))
                    expect(ssl._create_unverified_context.called).to(be(False))

        with context('insecure'):
            with it('uses insecure ssl context'):
                with patch('ssl._create_unverified_context', return_value = ssl._create_unverified_context()):
                    c = kerio.api.Client(url = 'https://1.1.1.1/api', insecure = True)
                    expect(ssl._create_unverified_context.called).to(be(True))

        with context('debug'):
            with it('enables debug output'):
                with \
                    patch('kerio.api.session.pprint'), \
                    patch('sys.stdout') as stdout:

                        c = kerio.api.Client(url = 'https://1.1.1.1/api', debug = True)

                        c.request(a = '1', b = '2')
                        expect(kerio.api.session.pprint.call_count).to(be(2))
                        expect(sys.stdout.write.call_count).to(be(4))

    with description('json_method'):
        with context('successfull run'):
            with it('logs in and sends authenticated requests'):

                # Session.login sets cookie and returns token, both must be present in subsequent request
                cookie = 'kookie'
                token  = 'sekret'

                httpretty.register_uri(
                    httpretty.POST,
                    'https://1.1.1.1/api',
                    body = json.dumps(
                        {
                            "result": {'token': token},
                            "jsonrpc": "2.0",
                            "id": 1,
                        }
                    ),
                    adding_headers = {
                        'set-cookie': cookie,
                    },
                )

                c = kerio.api.Client(url = 'https://1.1.1.1/api')

                r = c.Session.login(userName = 'u', password = 'p', application = {'name': "", 'vendor': "", 'version': ""})

                body = json.loads(httpretty.last_request().body)

                expect(body).to(have_key('method', 'Session.login'))
                expect(body['params']).to(have_key('userName', 'u'))
                expect(body['params']).to(have_key('password', 'p'))
                expect(body['params']).to(have_key('application'))

                result = ':-)'
                httpretty.register_uri(
                    httpretty.POST,
                    'https://1.1.1.1/api',
                    body = json.dumps(
                        {
                            "result": result,
                            "jsonrpc": "2.0",
                            "id": 1,
                        }
                    ),
                )

                response = c.request(a = '1', b = '2')
                expect(response).to(equal(result))

                body = json.loads(httpretty.last_request().body)

                expect(body).to(have_key('method', 'request'))
                expect(body).to(have_key('params'))
                expect(body).to(have_key('id', 1))
                expect(body).to(have_key('token', token))

                expect(httpretty.last_request().headers['x-token']).to(equal(token))
                expect(httpretty.last_request().headers['cookie']).to(equal(cookie))

                expect(httpretty.last_request().method).to(equal("POST"))
        
        with context('multiple levels method name'):
            with it('formats method name correctly'):
                c = kerio.api.Client(url = 'https://1.1.1.1/api')

                c.a.b.c.d.e.f.g.h(a = '1', b = '2')
                body = json.loads(httpretty.last_request().body)

                expect(body).to(have_key('method', 'a.b.c.d.e.f.g.h'))

        with context('error response'):
            with it('raises kerio.api.Error'):
                httpretty.register_uri(
                    httpretty.POST,
                    'https://1.1.1.1/api',
                    body = json.dumps(
                        {
                            "error": {'message': ':-('},
                            "jsonrpc": "2.0",
                            "id": 1,
                        }
                    ),
                )
                c = kerio.api.Client(url = 'https://1.1.1.1/api')

                expect(c.request).to(raise_error(kerio.api.Error, 'Http code: 200, json-rpc message: :-('))

    with description('upload'):
        with it('uploads file'):

            result = ':-)'
            httpretty.register_uri(
                httpretty.POST,
                'https://1.1.1.1/api/upload',
                body = json.dumps(
                    {
                        "result": result,
                        "jsonrpc": "2.0",
                        "id": 1,
                    }
                ),
            )

            with patch('kerio.api.method.open', mock_open(read_data = 'my data')) as mo:

                c = kerio.api.Client(url = 'https://1.1.1.1/api')

                expect(c.upload('./file')).to(equal(result))

                expect(httpretty.last_request().body).to(match(r'my data'))

    with description('download'):
        with it('downloads file'):

            data = 'my data'
            httpretty.register_uri(
                httpretty.GET,
                'https://1.1.1.1/download/file',
                body = data,
            )

            c = kerio.api.Client(url = 'https://1.1.1.1/api')
            result = c.download('/download/file')

            expect(result.next()).to(equal(data))
