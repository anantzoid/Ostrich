from app import webapp
from app.models import Order
from flask import request, jsonify

@webapp.route('/order', methods=['POST'])
def OrderItem():
    item_id = int(request.form['item_id'])
    user_id = int(request.form['user_id'])

    order = Order(item_id, user_id)
    order_id = order.placeOrder()

    return jsonify(order_id = order_id)
