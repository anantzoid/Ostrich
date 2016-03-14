#! /usr/bin/env python
#
# Mixpanel, Inc. -- http://mixpanel.com/
#
# Python API client library to consume mixpanel.com analytics data.

import hashlib
import urllib
import requests
import time
import MySQLdb
import json
import jsonl
from app import mysql, webapp


class Mixpanel(object):

    ENDPOINT = 'http://data.mixpanel.com/api'
    VERSION = '2.0'

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        
    def request(self, methods, params):
        """
            methods - List of methods to be joined, e.g. ['events', 'properties', 'values']
                      will give us http://mixpanel.com/api/2.0/events/properties/values/
            params - Extra parameters associated with method
        """
        params['api_key'] = self.api_key
        params['expire'] = int(time.time()) + 600   # Grant this request 10 minutes.

        if 'sig' in params: del params['sig']
        params['sig'] = self.hash_args(params)

        request_url = '/'.join([self.ENDPOINT, str(self.VERSION)] + methods) + '/?' + self.unicode_urlencode(params)
        request = requests.get(request_url)
        return [json.loads(_) for _ in request.text.split('\n') if _]

    def unicode_urlencode(self, params):
        """
            Convert lists to JSON encoded strings, and correctly handle any 
            unicode URL parameters.
        """
        if isinstance(params, dict):
            params = params.items()
        for i, param in enumerate(params):
            if isinstance(param[1], list): 
                params[i] = (param[0], json.dumps(param[1]),)

        return urllib.urlencode(
            [(k, isinstance(v, unicode) and v.encode('utf-8') or v) for k, v in params]
        )

    def hash_args(self, args, secret=None):
        """
            Hashes arguments by joining key=value pairs, appending a secret, and 
            then taking the MD5 hex digest.
        """
        for a in args:
            if isinstance(args[a], list): args[a] = json.dumps(args[a])

        args_joined = ''
        for a in sorted(args.keys()):
            if isinstance(a, unicode):
                args_joined += a.encode('utf-8')
            else:
                args_joined += str(a)

            args_joined += '='

            if isinstance(args[a], unicode):
                args_joined += args[a].encode('utf-8')
            else:
                args_joined += str(args[a])

        hash = hashlib.md5(args_joined)

        if secret:
            hash.update(secret)
        elif self.api_secret:
            hash.update(self.api_secret)
        return hash.hexdigest() 

def import_data(from_date, to_date):
    #NOTE date check if results get limited
    api_key = webapp.config['MIXPANEL_API_KEY']
    api_secret = webapp.config['MIXPANEL_API_SECRET']

    api = Mixpanel(
        api_key = api_key, 
        api_secret = api_secret
    )
    data = api.request(['export'], {
        'event': ['Duration_Home'],
        'from_date': from_date,
        'to_date': to_date,
        #'where': ''
        })  
    users_data = []
    for row in data:
        try:
            if not row['properties']['distinct_id'].isdigit():
                users_data.append([row['properties']['distinct_id'], row['properties']['Gcm Id']])
        except:
            continue
    users_data = [list(_) for _ in set(tuple(_) for _ in users_data)]

    conn = mysql.connect()
    cursor = conn.cursor()
    for row in users_data:
        cursor.except("""SELECT COUNT(*) FROM users_unregistered WHERE mixpanel_id = %s""",
                (row[0],))
        if cursor.fetchone()[0]:
            cursor.execute("""UPDATE users_unregistered SET gcm_id = %s, date_created = CURRENT_TIMESTAMP
                    WHERE mixpanel_id = %s""", tuple(row[::-1]))
        else:
            cursor.execute("""INSERT INTO users_unregistered (mixpanel_id, gcm_id) VALUES 
                    (%s, %s)""", tuple(row))
        conn.commit()
    return True
