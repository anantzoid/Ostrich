from app import webapp
from app.models import Admin, Item, Order, Utils, Lend
from flask import request
from flask.ext.jsonpify import jsonify

@webapp.route('/currentOrders')
def getCurrentOrders():
    current_order = Admin.getCurrentOrders()
    return jsonify(orders=current_order)

@webapp.route('/fetchInventoryDetail/<int:inventory_id>')
def fetchItemDetail(inventory_id):
    inv_data = Admin.getItemDetail(inventory_id)
    return jsonify(inv_data)

@webapp.route('/setInventoryData')
def setInventoryData():
    Admin.setInventoryData(request.args)
    return jsonify(status=True)

@webapp.route('/currentRentals')
def getCurrentRentals():
    current_rentals = Admin.getCurrentRentals()
    return jsonify(orders=current_rentals)

@webapp.route('/getPickups')
def getPickups():
    pickups = Admin.getPickups()
    return jsonify(orders=pickups)

@webapp.route('/removeItem')
def removeItem():
    item_ids = [int(_) for _ in request.args.get('item_id').split(",")]
    for item_id in item_ids:
        Item.removeItem(item_id)
    return jsonify({'status': 'True'})

@webapp.route('/deleteOrder', methods=['POST'])
def deleteOrder():
    orders = [int(_) for _ in request.form['order_id'].split(",")]
    for order in orders:
        Order.deleteOrder(order)
    return jsonify(status=True)

'''
    Update status of order in various status
    Statuses defined in getOrderStatusDetails method in order model
    @params
    order_id, status_id

'''
@webapp.route('/updateOrderStatus', methods=['GET'])
def updateOrderStatus():
    response = {'status': 'false', 'message': 'Wrong Status Id'}

    order_id = Utils.getParam(request.args, 'order_id', 'int')
    status_id = Utils.getParam(request.args, 'status_id', 'int')
    order_type = Utils.getParam(request.args, 'order_type')
    # Asking for user_id to double check
    if not(order_id and status_id):
        return Utils.errorResponse(response, webapp.config['HTTP_STATUS_CODE_DATA_MISSING'])
    if order_type not in ['borrow', 'lend']:
        return Utils.errorResponse(response, webapp.config['HTTP_STATUS_CODE_DATA_MISSING'])
    
    if order_type == 'borrow':
        if Order.getOrderStatusDetails(status_id):
            order_info = Order(order_id).updateOrderStatus(status_id)
            return jsonify({'order': order_info})
    else:
        if Lend.updateLendStatus(order_id, status_id):
            return jsonify({'status':'true'})
            
    return Utils.errorResponse(response)



