import os
from app import webapp
from flask import request, jsonify, render_template
from react.render import render_component

base_view = 'index.html'
components_path = os.path.join(os.getcwd(), 'app', 'static', 'js', 'components')
def path(js_file):
    return os.path.join(components_path, js_file)

@webapp.route('/')
def homepage():
    rendered = render_component(path('home.jsx'))
    return render_template(base_view, rendered=rendered)

