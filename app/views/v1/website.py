import os
from app import webapp
from app.models import *
import requests
import json
from flask import request, jsonify, render_template, redirect, url_for, session
from react.render import render_component

from apiclient import discovery
import httplib2
from oauth2client import client

components_path = os.path.join(os.getcwd(), 'app', 'static', 'js', 'components')

def path(js_file):
    return os.path.join(components_path, js_file)

def getTitle(path):
    if (path == 'home'):
        return 'Ostrich: Home'
    return 'Ostrich'

@webapp.route('/')
def homepage():
    view_component = 'home.jsx'
    collections = Collection.getHomepageCollections() 
    user_data = session.get('_user', None)
    props = {
        'collections': collections, 
        'user': user_data
    }
    store = {
        'component': view_component,  
        'props': json.dumps(props)
    }
    rendered = render_component(path(view_component), props=props)
    return render_template('index.html', 
            rendered=rendered, 
            title=getTitle('home'), 
            store=store)

@webapp.route('/googlesignin', methods=['POST'])
def googlesignin():
    auth_code = Utils.getParam(request.form, 'data', '')
    if not auth_code:
        return ''
    client_secret_file = '/etc/ostrich_conf/google_client_secret.json' 
    credentials = client.credentials_from_clientsecrets_and_code(
           client_secret_file,
           ['profile', 'email'],
           auth_code)
    http_auth = credentials.authorize(httplib2.Http())
    users_service = discovery.build('oauth2', 'v2', http=http_auth)
    user_document = users_service.userinfo().get().execute()
    user_data = {
        'username': user_document['email'],
        'name': user_document['name'],
        'email': user_document['email'],
        'google_id': credentials.id_token['sub']
        }
    user = User.createUser(user_data)
    session['_user'] = user
    visible_user_data = {
            'name': user['name']
            }
    return jsonify(data=visible_user_data)

'''
# Old google auth flow using tokeninfo and signIn listener (client)

@webapp.route('/1googlesignin', methods=['POST'])
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

'''
