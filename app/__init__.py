import os, sys
from flask import Flask
from flaskext.mysql import MySQL
from flask.ext.cors import CORS
from flask_mail import Mail

webapp = Flask(__name__)

mysql = MySQL()
cors = CORS(webapp)

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
