import os, sys
from flask import Flask
from flaskext.mysql import MySQL
from flask.ext.cors import CORS
from flask_mail import Mail
from flask.ext.session import Session
from flask.ext.cache import Cache

webapp = Flask(__name__)
#webapp.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

mysql = MySQL()

webapp.config.from_pyfile('/etc/ostrich_conf/app_config.cfg', silent=True)

#initialize global objects of libraries
mysql.init_app(webapp)
mail = Mail(webapp)
#cache = Cache(app)
Session(webapp)

if webapp.config['APP_ENV'] == 'dev':
    webapp.config['HOST'] = 'http://localhost:5000'
else:
    webapp.config['HOST'] = 'http://52.32.104.299'

import app.models
import app.views

cache = app.models.cache.Cache()

