#!/usr/bin/env python

import kerio.api
from pprint import pprint

client = kerio.api.Client(debug = True, insecure = True, url = 'https://localhost:4021/admin/api/jsonrpc/')

def init():
    client.ProductActivation.activate(
        adminPassword = "password",
        adminLanguage = "en",
        adminEmail = "admin@my.company.net",
        pbxLanguageId = 2,
        pbxStartingNumber = "10",
        timeZoneId = "",
        reboot = False,
        sendClientStatistics = False,
        myKerioEnabled = False,
    )

#init()

client.Session.login(userName = 'Admin', password = 'password', application = {'name': "", 'vendor': "", 'version': ""})
client.upload('./test-connect.py')
client.Session.logout()

try:
    client.Session.logout()
except kerio.api.Error, e:
    pprint(e)

