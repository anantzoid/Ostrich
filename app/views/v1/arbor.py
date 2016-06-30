from flask import request, jsonify, render_template, redirect, url_for
from react.render import render_component
from app import webapp
from app.models import *
from app.decorators import user_session
from app.views.v1.website import path
    
@webapp.route('/paypal/')
@user_session
def arbor_index(**kwargs):
    client = request.path.strip("/").title()
    store = {}
    props = kwargs['props']
    props.update({
        'client': client,
        'page': 'arbor'
        })

    if not props['user']:
        store['component'] = 'arborLogin.jsx'
        rendered = render_component(path(store['component']), props=props)
    else:
        store['component'] = 'arborHome.jsx'
        props['books'] = Arbor.getArborBooks(client)
        rendered = render_component(path(store['component']), props=props)

    store['props'] = props
    return render_template('index.html',
            rendered=rendered,
            title='%s Arbor' % client,
            store=store)

@webapp.route('/paypal/orders/')
@user_session
def arbor_orders(**kwargs):
    if not kwargs['props']['user']:
        return redirect(url_for('arbor_index'))

    if not kwargs['props']['user']['is_admin']:
        return redirect(url_for('arbor_index'))

    client = request.path.strip("/").split("/")[0].title()
    store = {}
    store['component'] = 'arborOrders.jsx'
    props = kwargs['props']
    props.update({
        'client': client,
        'orders': Arbor.getUserOrders(props['user']['user_id']),
        'page': 'arbor_orders'
        })
    rendered = render_component(path(store['component']), props=props)
    store['props'] = props

    return render_template('index.html',
            rendered=rendered,
            title='%s Arbor Orders' %client,
            store=store)

@webapp.route('/paypal/admin/')
@user_session
def arbor_admin(**kwargs):
    if not kwargs['props']['user']:
        return redirect(url_for('arbor_index'))

    if not kwargs['props']['user']['is_admin']:
        return redirect(url_for('arbor_index'))
    
    client = request.path.strip("/").split("/")[0].title()
    store = {}
    store['component'] = 'arborAdmin.jsx'
    props = kwargs['props']
    props.update({
        'client': client,
        'items': Arbor.getInventoryItems(client),
        'page': 'arbor_admin'
        })
    rendered = render_component(path(store['component']), props=props)
    store['props'] = props

    return render_template('index.html',
            rendered=rendered,
            title='%s Arbor Admin' %client,
            store=store)

@webapp.route('/arbor/checkout', methods=['POST'])
@user_session
def arbor_checkout(**kwargs):
    response = {'status': False, 'message': 'Something went wrong'}
    if not kwargs['props']['user']:
        return jsonify(response)

    user_id = Utils.getParam(request.form, 'user_id', 'int')
    if kwargs['props']['user']['user_id'] !=  user_id:
        return jsonify(response)

    arbor_id = Utils.getParam(request.form, 'arbor_id')
   
    status = Arbor.checkout(user_id, arbor_id)
    if not status:
        response['message'] = 'Sorry, that book is no longer available.'
    else:
        response['status'] = True
        response['message'] = 'Success! Please pick up the book from the library.'

    return jsonify(response)
