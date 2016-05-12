import os, sys
from flask import Flask
from flaskext.mysql import MySQL
from flask.ext.cors import CORS
from flask_mail import Mail

webapp = Flask(__name__)
#webapp.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

mysql = MySQL()
#TODO shift resources to @cross_origin
#cors = CORS(webapp, resources={'/*/?':{'origins':'*'}, '/preregister':{'origins':'*', 'supports_credentials':'true', 'expose_headers': 'accept, authorization', 'methods':'GET'}})

webapp.config.from_pyfile('/etc/app_config.cfg', silent=True)

#initialize global objects of libraries
mysql.init_app(webapp)
mail = Mail(webapp)

# NOTE temp workaround as cache is low priority
if webapp.config['APP_ENV'] == 'dev':
    from werkzeug.contrib.cache import SimpleCache
    cache = SimpleCache()
    from flask.ext.cors import CORS
    CORS(webapp)
else:
    from werkzeug.contrib.cache import MemcachedCache
    cache = MemcachedCache(['127.0.0.1:11211'])

import app.views
import app.models

@webapp.route('/')
def hello():
    return 'Index Page'
