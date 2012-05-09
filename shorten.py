#!/usr/bin/env python2

import json

from sys import argv
from urllib2 import urlopen, Request

shortener = argv[1]
url = argv[2]
custom_code = argv[3] if len(argv) > 3 else None

if shortener[-1] != '/':
    shortener = shortener + '/'

request = {'long_url': url}
if custom_code:
    request['custom_short_code'] = custom_code

r = Request(shortener + 'shorten_url', json.dumps(request), headers={"Content-Type": "application/json"})

reply = json.load(urlopen(r))

print reply

if reply['success']:
    print shortener + reply['short_code']

