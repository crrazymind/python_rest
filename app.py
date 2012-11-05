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

connection_string = "mongodb://localhost"


@get('/')
def index():
    return bottle.template("index")


@get('/hello')
def hello_page():
    return bottle.template("index")


@get('/api')
def api():
    return bottle.template("")

bottle.debug(True)

port = int(os.environ.get("PORT", 5000))
bottle.run(host='0.0.0.0', port=port)
