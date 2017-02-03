#!/usr/bin/env python

import kerio.api
from pprint import pprint

client = kerio.api.Client()

client.Session()
client.Session.login(x = 1, y = 2)
