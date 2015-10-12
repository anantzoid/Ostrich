import os, sys
from flask import Flask
from flaskext.mysql import MySQL

webapp = Flask(__name__)
mysql = MySQL()

if os.environ.get('APP_ENV') == 'dev':
    #TODO change for production
    webapp.config.from_pyfile('../config.cfg', silent=True)
else:
    webapp.config.from_pyfile('../config.cfg', silent=True)


#initialize global objects of libraries
mysql.init_app(webapp)

import app.views
import app.models

@webapp.route('/')
def hello():
    return 'Index Page'
