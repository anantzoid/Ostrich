from app import mysql
from pymongo import MongoClient
from app.models import Utils, Mailer
from datetime import date, timedelta
from app import webapp
import json
from collections import OrderedDict

def user_followup():
    client = MongoClient(webapp.config['MONGO_DB'])
    db = client.ostrich
    cursor = mysql.connect().cursor()

    ts = str(date.today() - timedelta(1))
    cursor.execute(""" select user_id, name, phone, date_created from users
                        where DATE(date_created) = %s and
                        user_id not in (select distinct user_id from orders) """, (ts,))
    users = []
    for i in range(cursor.rowcount):
        users.append(OrderedDict(Utils.fetchOneAssoc(cursor)))

    for user in users:
        distinct_q = []
        cursor.execute("""select query, timestamp from search_fails where user_id = %s""", (user['user_id'],))
        user['fails'] = []
        for i in range(cursor.rowcount):
            q = Utils.fetchOneAssoc(cursor)
            if q['query'] not in distinct_q:
                user['fails'].append(q)
                distinct_q.append(q['query'])

        user['searches'] = []
        for query in db.search_log.find({"user_id": str(user['user_id'])}):
            if query['q'] not in distinct_q:
                user['searches'].append({
                    "query": query['q'],
                    "timestamp": str(query['timestamp'])
                    })
                distinct_q.append(query['q'])

    if users:
        users = json.dumps({'users': users}, indent=4)
        Mailer.genericMailer({'subject': 'Dropped Users for '+str(ts), 'body': users},
                    recipients=['divyankjn@gmail.com', 'achal.kothari@gmail.com'])
