import bottle

import pymongo
import cgi
import re
import datetime
import random
import hmac
import user
import json
import sys
from bottle import get, post, request
from bson import BSON
from bson import json_util

#connection_string = "mongodb://localhost"
connection_string = "mongodb://admin:mongo_admin@staff.mongohq.com:10009/app3605825"
connection = pymongo.Connection(connection_string, safe=True)
db = connection['app3605825']


@get('/')
def index():
    return bottle.template("index")


@get('/hello')
def hello_page():
    return bottle.template("index")


def makeJson(data):
    return json.dumps(data, sort_keys=True, indent=4, default=json_util.default)


@get('/api')
def api():
    #data = db.items.find_one({'title': 'Meanwhile in India...'})
    result = []
    data = db.items.find()
    for item in data:
        result.append(makeJson(item))
    return result


@post('/api')
def api_insert():
    print 'processing post here:'
    print bottle.request.content_type
    print bottle.request.json
    if bottle.request.json:
        db.items.insert(bottle.request.json)
    return bottle.request.json


@bottle.put('/api/*')
def api_put():
    print 'put here'
    print bottle.request.content_type
    if bottle.request.json:
        #data = {'name': 'qwe'}
        for item in bottle.request.json:
            db.items.update({'_id': item['_id']}, {item})
    return bottle.request.json


bottle.debug(True)
#port = int(os.environ.get("PORT", 5000))
port = 5000
#bottle.run(host='0.0.0.0', port=port)
bottle.run(host='127.0.0.1', port=port)
