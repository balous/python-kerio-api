#!/usr/bin/env python

import kerio.api
from pprint import pprint

client = kerio.api.Client(debug = True, insecure = True, url = 'https://localhost:4040/admin/api/jsonrpc')

#client.Init.setHostname(hostname = 'host-name')
#client.Init.createPrimaryDomain(domainName = "domain.com")
#client.Init.createAdministratorAccount(loginName = "Admin", password = 'password')
#client.Init.finish()

client.Session.login(userName = 'Admin', password = 'password', application = {'name': "", 'vendor': "", 'version': ""})
client.upload('./test.py')
client.Session.logout()

try:
    client.Session.logout()
except kerio.api.Error, e:
    pprint(e)

