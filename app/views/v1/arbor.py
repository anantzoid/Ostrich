from flask import request, jsonify, render_template, redirect
from react.render import render_component
from app import webapp
from app.models import *
from app.decorators import user_session
from app.views.v1.website import path
    
@webapp.route('/paypal')
@user_session
def arbor_index(**kwargs):
    client = request.path.strip("/").title()
    store = {}
    props = kwargs['props']
    props.update({'client': client})

    if not props['user']:
        store['component'] = 'arborLogin.jsx'
        rendered = render_component(path(store['component']), props=props)
    else:
        store['component'] = 'arborHome.jsx'
        props['books'] = Item.getArborBooks(client)
        rendered = render_component(path(store['component']), props=props)

    store['props'] = props
    return render_template('index.html',
            rendered=rendered,
            title='%s Arbor' % client,
            store=store)


