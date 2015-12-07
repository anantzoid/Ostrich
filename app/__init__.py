import os, sys
from flask import Flask
from flaskext.mysql import MySQL
from flask.ext.cors import CORS
from flask_mail import Mail

webapp = Flask(__name__)

mysql = MySQL()
cors = CORS(webapp)
mail = Mail(webapp)

if os.environ.get('APP_ENV') == 'dev':
    #TODO change for production
    webapp.config.from_pyfile('../config/config.cfg', silent=True)
else:
    webapp.config.from_pyfile('../config/config_prod.cfg', silent=True)

#initialize global objects of libraries
mysql.init_app(webapp)

import app.views
import app.models

@webapp.route('/')
def hello():
    return 'Index Page'
