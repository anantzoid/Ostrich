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


@webapp.route('/lend', methods=['POST'])
def lendItem():
    response = {'status': 'False'}
    lend_data = {}

    lend_data['item_id'] = Helpers.getParam(request.form, 'item_id')
    lend_data['user_id'] = Helpers.getParam(request.form, 'user_id')

    #incentive info will have delivery date (depending on period of rental)
    lend_data['incentive_id'] = Helpers.getParam(request.form, 'incentive_id ')
    lend_data['delivery_slot'] = Helpers.getParam(request.form, 'delivery_slot')

    #for pickup
    lend_data['pickup_date'] = Helpers.getParam(request.form, 'pickup_date')
    lend_data['pickup_slot'] = Helpers.getParam(request.form, 'pickup_slot')
  
    for key in lend_data:
        if not lend_data[key]:
            response['message'] = key+' missing'
            return jsonify(response)

    inventory_id = Order.lendItem(lend_data)
   
    if inventory_id:
        response['status'] = 'True'
        response['inventory_id'] = inventory_id

    return response


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


