from app import webapp
from app.models import Order, Lend, Item, Utils
from flask import request, jsonify
from app.models import Notifications
import json

'''
    Make order call
    @params
        item_id,
        user_id,
        address_id

        optional:
        payment_mode: {cash, wallet} (for now)
        order_return: Y-m-d

    @response
        status
        message: on error
        order_id: on success

'''
@webapp.route('/order', methods=['POST'])
def OrderItem():
   
    order_data = {}
    for key in request.form:
        order_data[key] = request.form[key]

    order_placed = Order.placeOrder(order_data)

    if 'order_id' in order_placed and order_placed['order_id']:
        order_placed['status'] = 'True'
        return jsonify(order_placed)
    else:
        if isinstance(order_placed, dict):
            return Utils.errorResponse(order_placed)
        else:
            return Utils.errorResponse(order_placed[0], order_placed[1])
            

'''
    Put an item on rent
    @params
        user_id: The current user's id
        item_id: The item's id (correspoding to the DB)
        pickup_date: Y-m-d H:i:s 
        pickup_slot: slot id for picking up from user
        delivery_date: Date of delivery back
        delivery_slot: time slot id for delivring back the object
        item_condition: Description condition of item

    @response
        inventory_id(optional)
        message(optional)
'''
@webapp.route('/lend', methods=['POST'])
def lendItem():
    lend_data = {}
    for key in request.form:
        lend_data[key] = request.form[key]
    lend_info = Lend.lendItem(lend_data)

    if 'inventory_id' in lend_info and lend_info['inventory_id']:
        return jsonify(lend_info)
    else:
        if isinstance(order_placed, dict):
            return Utils.errorResponse(lend_info)
        else:
            return Utils.errorResponse(lend_info[0], lend_info[1])

'''
    Get the status of a current order
    @params
        user_id: The current user's id
        order_id: The order id received on placing the order

    @response
      on success:
      item: item snippet
      status_details : {Status, Description}

      on error:
      status
'''
@webapp.route('/orderStatus', methods=['POST'])
def orderStatus():
    response = {"status": "False"}

    user_id = Utils.getParam(request.form, 'user_id', 'int')
    order_id = Utils.getParam(request.form, 'order_id', 'int')

    # Asking for user_id to double check
    if not(user_id and order_id):
        return Utils.errorResponse(response, webapp.config['HTTP_STATUS_CODE_DATA_MISSING'])

    order = Order(order_id)
    order_status = order.getOrderStatusForUser(user_id)
   
    if order_status:
        response = order_status
        return jsonify(response)
    else:
        return Utils.errorResponse(response)

@webapp.route('/editOrderDetails', methods=['POST'])
def editOrderDetails():
    response = {'status': 'False'}
    order_id = Utils.getParam(request.form, 'order_id', 'int')
    if not order_id:
        return Utils.errorResponse(response, webapp.config['HTTP_STATUS_CODE_DATA_MISSING'])

    order_data = {}
    for key in request.form:
        order_data[key] = request.form[key]

    order = Order(order_id)
    status = order.editOrderDetails(order_data)
    if status:
        return jsonify(order.getOrderInfo(formatted=True))
    else:
        return Utils.errorResponse(response)


'''
    Request an item to be added to inventory if it's being put on rent
    @params
    item_type: books(for now)
    item_id: Item's unique ID in physical world
             eg. ISBN for books
    item_name

    @response
        status
'''
@webapp.route('/requestItem', methods=['POST'])
def requestItem():
    item_type = Utils.getParam(request.form, 'item_type')
    
    # ISBN in case of books
    #TODO look into this for genericity
    item_id = Utils.getParam(request.form, 'item_id')
    item_name = Utils.getParam(request.form, 'item_name')

    if not(item_name and item_type and item_id):
        return Utils.errorResponse({'status': 'False'}, webapp.config['HTTP_STATUS_CODE_DATA_MISSING'])

    Item.storeItemRequest(item_type, item_id, item_name)

    return jsonify(status='True')


'''
    Returns time slots for delivery
    @response
        list of time slot objects: [{
                                   'slot_id',
                                   'start_time',
                                   'end_time'
                                   }]
'''
@webapp.route('/getTimeSlot')
def getTimeSlot():
    return jsonify(time_slots=Order.getTimeSlotsForOrder())

'''
    Test API calls
'''
@webapp.route('/push', methods=['POST'])
def pushNotification():
    if 'gcm_id' in request.form:
        temp_gcm_id = request.form['gcm_id']
    else:
        temp_gcm_id = 'dTKtMjUPSho:APA91bGy3oVY680azB-jNmdAlDyRBCswnRaNg17naVkCXfTe88mSfJETB5BZTXO1dDaQJiCd7lUoDccJt3asT04nfWDj8gaghquqwjgIFUEuCZ2w4RojeTA4fQAsWNhVThSWWlASJ7NE'
    notification_data = json.loads(str(request.form['data']))
    status = Notifications(temp_gcm_id).sendNotification(notification_data)
    return jsonify(status)
