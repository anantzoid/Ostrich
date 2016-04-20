import os
from app import webapp
from app.models import *
from flask import request, jsonify, render_template
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
    
    rendered = render_component(path('home.jsx'), props={'panel_data': panel_data})
    title = getTitle('home')
    return render_template(base_view, rendered=rendered, title=title)

