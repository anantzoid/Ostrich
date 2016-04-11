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

import app.views
import app.models

@webapp.route('/')
def hello():
    from app.scripts.upsell_email import upsellEmail
    return upsellEmail(23)
    return 'Index Page'
