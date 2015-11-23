import os, sys
from flask import Flask
from flaskext.mysql import MySQL
from flask.ext.cors import CORS

webapp = Flask(__name__)
mysql = MySQL()

cors = CORS(webapp)

if os.environ.get('APP_ENV') == 'dev':
    #TODO change for production
    webapp.config.from_pyfile('../config.cfg', silent=True)
else:
    webapp.config.from_pyfile('../config.cfg', silent=True)

#TODO put in config file
webapp.config['http_status_code_data_missing'] = 400
webapp.config['http_status_code_entry_exists'] = 409
webapp.config['http_status_code_success'] = 200
webapp.config['http_status_code_error'] = 500

#initialize global objects of libraries
mysql.init_app(webapp)

import app.views
import app.models

@webapp.route('/')
def hello():
    return 'Index Page'
