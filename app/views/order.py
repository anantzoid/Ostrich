from app import webapp
from app.models import Order, Item, Helpers
from flask import request, jsonify

@webapp.route('/order', methods=['POST'])
def OrderItem():
    
    #TODO make return pattern consistent
    item_ids = request.form['item_id'] if 'item_id' in request.form else ''
    user_id = int(request.form['user_id']) if 'user_id' in request.form else ''
    address_id = int(request.form['address_id']) if 'address_id' in request.form else ''
  
    if not item_ids:
        return jsonify({'status':'False', 'message':'Item ids missing'})

    if not user_id:
        return jsonify({'status':'False', 'message':'User id missing'})

    if not address_id:
        return jsonify({'status':'False', 'message':'Address id missing'})

    item_ids = [int(item_id) for item_id in item_ids.split(',')]
    order_placed = Order.placeOrder(item_ids, user_id, address_id)

    if 'order_id' in order_placed:
        order_placed['status'] = 'True'
    else:
        order_placed['status'] = 'False'

    return jsonify(order_placed)

@webapp.route('/requestItem', methods=['POST'])
def requestItem():
    item_type = Helpers.getParam(request.form, 'item_type')
    
    # ISBN in case of books
    #TODO look into this for genericity
    item_id = Helpers.getParam(request.form, 'item_id')
    item_name = Helpers.getParam(request.form, 'item_name')

    Item.storeItemRequest(isbn, item_name, itemp_type)

@webapp.route('/getRentalRate')
def getRentalRate():
    return None

@webapp.route('/getIncentiveSlab')
def getIncentiveSlab():
    return None

@webapp.route('/getTimeSlot')
def getTimeSlot():
    return jsonify(time_slots=Order.getTimeSlot())
