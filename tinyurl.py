#!/usr/bin/env python2

import bottle
import json
import random
import sqlite3
import string

bottle.debug(True)

# The list of valid characters in an URL code: [a-zA-Z0-9]
URL_CODE_CHARS = string.ascii_letters + string.digits

class UrlDB:
    def __init__(self):
        self.con = None

    def connect(self):
        self.con = sqlite3.connect("urls.db")
        self.con.execute("CREATE TABLE IF NOT EXISTS urls (id PRIMARY KEY ON CONFLICT FAIL, url)")

    def get_url(self, url_code):
        '''Get long URL from shortened code

        Returns None if no entry exists'''
        for row in self.con.execute("SELECT url FROM urls WHERE id = ?", (url_code,)):
            return row[0]

        return None

    def store_url(self, long_url, url_code=None):
        '''Generate a new unique URL code

        If url_code is specified and it conflicts with an existing code,
        returns None. Otherwise, returned the generated or given URL code.
        '''
        new_code = None
        while True:
            try:
                with self.con:
                    new_code = self.random_code() if (url_code == None) else url_code
                    self.con.execute("INSERT INTO urls(id, url) values (?, ?)",
                                     (new_code, long_url))
                    break
            except sqlite3.IntegrityError:
                if url_code != None:
                    return None

        return new_code

    @staticmethod
    def random_code():
        return ''.join(random.choice(URL_CODE_CHARS) for x in xrange(6))
        
    
db = UrlDB()
db.connect()

@bottle.post('/shorten_url')
def new_url():
    request = json.load(bottle.request.body)
    url_code = db.store_url(request['long_url'], request.get('custom_short_code', None))

    if url_code:
        return {'success': True, 'short_code': url_code}
    else:
        return {'success': False}


@bottle.route('/<url_code:re:.+$>')
def get_long_url(url_code):
    long_url = db.get_url(url_code)

    if not long_url:
        bottle.abort(404, "No such URL")

    bottle.redirect(long_url)


if __name__ == '__main__':
    bottle.run(host='localhost', port=8080, reloader=True)
