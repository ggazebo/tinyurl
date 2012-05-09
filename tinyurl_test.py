#!/usr/bin/env python2

import json
import os
import re
import urllib2

import tinyurl

from urllib2 import urlopen, Request

TEST_DB_PATH="./_test.db"

SHORTENER = "http://127.0.0.1:8080/"
SHORTEN_URL = SHORTENER + "shorten_url"

'''
print "STORE 'yangman' => 'http://yangman.ca'"
for l in  urlopen(Request(SHORTEN_URL, json.dumps({'long_url': "http://yangman.ca", 'custom_short_code': 'yangman'}),
                     headers={"Content-Type": "application/json"})):
    print l

print "STORE 'http://tinyco.com' => random"
for l in  urlopen(Request(SHORTEN_URL, json.dumps({'long_url': "http://tinyco.com"}),
                     headers={"Content-Type": "application/json"})):
    print l
'''

def test_code_generator():
    print "Checking conformity of randomly generated codes:"

    r = re.compile(r"^[a-zA-Z0-9]{6}$")

    for x in xrange(6):
        code = tinyurl.UrlDB.random_code()

        passes = (r.match(code) != None)

        print "  %s : %s" % (code, "pass" if passes else "FAIL")

        if not passes:
            return False

    return True


def test_db():
    print "Testing DB class:"

    try:
        os.remove(TEST_DB_PATH)
    except OSError:
        pass
    db = tinyurl.UrlDB(TEST_DB_PATH)
    db.connect()

    passes = False
    custom_code = 'test'

    print "  New URL with custom code :", 
    result = db.store_url("http://test.com/", "test")
    if result == custom_code:
        print "pass"
    else:
        print "FAIL"
        return False
    
    print "  New URL with conflicting code :", 
    result = db.store_url("http://foo.com/", "test")
    if result == None:
        print "pass"
    else:
        print "FAIL"
        return False
    
    print "  Fetch valid URL :", 
    result = db.get_url("test")
    if result == "http://test.com/":
        print "pass"
    else:
        print "FAIL"
        return False
    
    print "  Fetch invalid URL :", 
    result = db.get_url("foo")
    if result == None:
        print "pass"
    else:
        print "FAIL"
        return False

    print "  Store to random code :", 
    code = db.store_url("http://foo.com/")
    if code:
        print "pass (%s)" % code
    else:
        print "FAIL"
        return False

    print "  Fetch valid URL using random code :",
    result = db.get_url(code)
    if result == "http://foo.com/":
        print "pass"
    else:
        print "FAIL"
        return False

    print "  New URL with unusual characters in short code :",
    result = db.store_url("http://test.com/", "a^$:@;'%")
    if result == "a^$:@;'%":
        print "pass"
    else:
        print "FAIL"
        return False

    print "  Fetch valid URL using unusual characters in short code code :",
    result = db.get_url("a^$:@;'%")
    if result == "http://test.com/":
        print "pass"
    else:
        print "FAIL"
        return False

    os.remove(TEST_DB_PATH)
    return True


test_code_generator()
test_db()
