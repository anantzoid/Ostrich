from app import webapp
from app.models import Order
from flask import request, jsonify

@webapp.route('/order', methods=['POST'])
def OrderItem():
    item_id = int(request.form['item_id'])
    user_id = int(request.form['user_id'])

    order = Order(item_id, user_id)
    order_placed = order.placeOrder()

    if 'order_id' in order_placed:
        order_placed['status'] = 'True'
    else:
        order_placed['status'] = 'False'

    return jsonify(order_placed)

