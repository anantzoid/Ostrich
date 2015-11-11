from app import webapp
from app.models import Order, Item, Utils
from flask import request, jsonify

@webapp.route('/order', methods=['POST'])
def OrderItem():
   
    order_data = {}
    for key in request.form:
        order_data[key] = request.form[key]

    order_placed = Order.placeOrder(order_data)

    if 'order_id' in order_placed:
        order_placed['status'] = 'True'
    else:
        order_placed['status'] = 'False'

    return jsonify(order_placed)


@webapp.route('/lend', methods=['POST'])
def lendItem():
    response = {'status': 'False'}
    lend_data = {}

    lend_data['item_id'] = Utils.getParam(request.form, 'item_id')
    lend_data['user_id'] = Utils.getParam(request.form, 'user_id')

    #incentive info will have delivery date (depending on period of rental)
    lend_data['incentive_id'] = Utils.getParam(request.form, 'incentive_id')
    lend_data['delivery_slot'] = Utils.getParam(request.form, 'delivery_slot')

    #for pickup
    lend_data['pickup_date'] = Utils.getParam(request.form, 'pickup_date')
    lend_data['pickup_slot'] = Utils.getParam(request.form, 'pickup_slot')

    lend_data['item_condition'] = Utils.getParam(request.form, 'item_condition')
  
    for key in lend_data:
        if not lend_data[key]:
            response['message'] = key+' missing'
            return jsonify(response)

    inventory_id = Order.lendItem(lend_data)
   
    if inventory_id:
        response['status'] = 'True'
        response['inventory_id'] = inventory_id

    return jsonify(response)

@webapp.route('/orderStatus', methods=['POST'])
def orderStatus():
    resp = {"status": "False"}

    user_id = Utils.getParam(request.form, 'user_id', 'int')
    order_id = Utils.getParam(request.form, 'order_id', 'int')

    # Asking for user_id to double check
    if not(user_id and order_id):
        return jsonify(resp)

    order = Order(int(order_id))
    order_status = order.getStatus(int(user_id))
   
    if not order_status:
        order_status = resp

    return jsonify(order_status)

@webapp.route('/requestItem', methods=['POST'])
def requestItem():
    item_type = Utils.getParam(request.form, 'item_type')
    
    # ISBN in case of books
    #TODO look into this for genericity
    item_id = Utils.getParam(request.form, 'item_id')
    item_name = Utils.getParam(request.form, 'item_name')

    if not(item_name and item_type and item_id):
        return jsonify({'status': 'False'})

    Item.storeItemRequest(item_type, item_id, item_name)

    return jsonify(status='True')

@webapp.route('/getRentalRate')
def getRentalRate():
    return None

@webapp.route('/getIncentiveSlab')
def getIncentiveSlab():
    return None

@webapp.route('/getTimeSlot')
def getTimeSlot():
    return jsonify(time_slots=Order.getTimeSlot())


