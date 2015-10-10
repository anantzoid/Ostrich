import os, sys
from flask import Flask

webapp = Flask(__name__)

if os.environ.get('APP_ENV') == 'dev':
    #TODO change for production
    webapp.config.from_pyfile('../config.cfg', silent=True)
else:
    webapp.config.from_pyfile('../config.cfg', silent=True)


#initialize global objects of libraries


import app.views
import app.models

@webapp.route('/')
def hello():
    return 'Hello'
