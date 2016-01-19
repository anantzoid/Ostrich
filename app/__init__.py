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
    from flask import render_template
    return render_template('welcome.html')
    return 'Index Page'
