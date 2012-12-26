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
import os
import ast
from itertools import izip
from bottle import get, post, request, put
from bson import BSON
from bson import json_util
from bson.objectid import ObjectId

#connection_string = "mongodb://localhost"
connection_string = "mongodb://admin:mongo_admin@staff.mongohq.com:10009/app3605825"
connection = pymongo.Connection(connection_string, safe=True)
db = connection['app3605825']
data_shema = ["cost", "done", "duration", "eta", "link", "title"]


@get('/')
def index():
    return bottle.template("index")


@get('/hello')
def hello_page():
    return bottle.template("index")


def makeJson(data):
    return json.dumps(data, sort_keys=True, indent=4, default=json_util.default)


def getAllJSONP(request, data):
    if request.query.get('callback'):
        bottle.response.content_type = 'application/json'
        data = ''.join(['%s,%s,' % (key, value) for (key, value) in data.items()])
        data = data.rstrip()
        return ''.join([request.query.get('callback'), '({items:[', data, ']})'])
    else:
        return data


def makeJSONP(request, data):
    if request.query.get('callback'):
        bottle.response.content_type = 'application/json'
        if type(data) is str:
            return ''.join([request.query.get('callback'), '(', data, ')'])
        else:
            data = ''.join(['%s,%s' % (key, value) for (key, value) in data.items()])
            data = data.rstrip()
            return ''.join([request.query.get('callback'), '({items:[', data, ']})'])
    else:
        return data


def chomp(t):
    return map(lambda s: s.strip(), t)


@get('/api')
def api():
    result = []
    #data = db.items_bb.find({}, {'title':1, 'cost':1, 'duration':1, 'eta':1, 'title':1,'_id':0})
    data = db.items_bb.find()
    for item in data:
        result.append(makeJson(item))
    i = iter(result)
    result = dict(izip(i, i))
    bottle.response.set_header('Access-Control-Allow-Origin', '*')
    print "plain get method called"
    return getAllJSONP(bottle.request, result)


@get('/api/<id>')
def api_other(id):
    print id
    result = []
    method = bottle.request.query.get("_method")
    #if not id:
        #print method
        #if method == "create":
        #    return createItem(bottle.request.query.get("items"))
        #else:
        #    return makeJSONP(bottle.request, result)
    data = bottle.request.query.get("items")
    bottle.response.set_header('Access-Control-Allow-Origin', '*')
    if method == "update":
        return updateItem(data, id)
    if method == "delete":
        return deleteItem(id)
    return makeJSONP(bottle.request, "console.log({status:'wrong _method parameter'})")


def createItem(data):
    data = json.loads(data)
    print ""
    print "about to create item "
    res = db.items_bb.insert(grabData(data))
    print res
    return makeJSONP(bottle.request, "console.log({status : '" + "23232" + " update was successful'})")


def updateItem(data, id):
    data = json.loads(data)
    print ""
    print "about to update item " + id
    res = db.items_bb.update({"_id": ObjectId(id)}, grabData(data))
    print res
    return makeJSONP(bottle.request, "console.log({status : '" + id + " update was successful'})")


def deleteItem(id):
    #data = json.loads(data)
    #print ""
    #print "about to update item " + id
    #res = db.items_bb.update({"_id": ObjectId(id)}, grabData(data))
    #print res
    return makeJSONP(bottle.request, "console.log({status : '" + id + " deleted'})")


def grabData(source):
    res = dict()
    for item in data_shema:
        res[item] = source[item]
    return res


def process_Json(json):
    print 'processing post here:'
    print bottle.request.content_type
    print bottle.request.json
    if bottle.request.json:
        db.items_bb.insert(bottle.request.json)
    bottle.response.set_header('Access-Control-Allow-Origin', '*')
    return bottle.request.json


@post('/api')
def api_insert():
    print 'processing post here:'
    print bottle.request.content_type
    print bottle.request.json
    if bottle.request.json:
        db.items_bb.insert(bottle.request.json)
    bottle.response.set_header('Access-Control-Allow-Origin', '*')
    return bottle.request.json


@bottle.put('/api')
def api_put():
    print 'put here'
    print bottle.request.content_type
    if bottle.request.json:
        #data = {'name': 'qwe'}
        for item in bottle.request.json:
            db.items_bb.update({'_id': item['_id']}, {item})
    bottle.response.set_header('Access-Control-Allow-Origin', '*')
    return bottle.request.json


bottle.debug(True)
port = int(os.environ.get("PORT", 5000))
bottle.run(host='0.0.0.0', port=port, reloader='true', interval=1)
#bottle.run(host='127.0.0.1', port=port)
