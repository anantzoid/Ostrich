import os
from app import webapp
from app.models import *
import requests
import json
from flask import request, jsonify, render_template, redirect, url_for, session
from react.render import render_component

base_view = 'index.html'
components_path = os.path.join(os.getcwd(), 'app', 'static', 'js', 'components')
def path(js_file):
    return os.path.join(components_path, js_file)

def getTitle(path):
    if (path == 'home'):
        return 'Ostrich: Home'
    return 'Ostrich'

@webapp.route('/')
def homepage():
    panel_data = [Collection(4).getExpandedObj(), Collection(5).getExpandedObj()]
    user_data = session.get('_user', None)
    if session.get('authenticated'):
        if not user_data:
            session['authenticated'] = False

    rendered = render_component(path('home.jsx'), props={
        'panel_data': panel_data, 
        'user': user_data
    })
    return render_template(base_view, rendered=rendered, title=getTitle('home'))

@webapp.route('/googlesignin', methods=['POST'])
def tokensignin():
    idtoken = Utils.getParam(request.form, 'data', '')
    if not idtoken:
        return False

    # TODO replace with apiclient
    req = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='+idtoken)
    resp = json.loads(req.text)
    if resp['aud'] == webapp.config['GOOGLE_AUTH_CLIENT_ID']:
        user_data = {
                'username': resp['email'],
                'name': resp['name'],
                'email': resp['email'],
                'google_id': resp['sub']
                }
        user = User.createUser(user_data)
        session['authenticated'] = True
        session['_user'] = user
        return jsonify(session['_user'])
    return jsonify({})

