from app import webapp
from app.models import *
from flask import request
from flask.ext.jsonpify import jsonify

@webapp.route('/push', methods=['POST'])
def pushNotification():
    if 'gcm_id' in request.form:
        temp_gcm_id = request.form['gcm_id']
    else:
        temp_gcm_id = 'dTKtMjUPSho:APA91bGy3oVY680azB-jNmdAlDyRBCswnRaNg17naVkCXfTe88mSfJETB5BZTXO1dDaQJiCd7lUoDccJt3asT04nfWDj8gaghquqwjgIFUEuCZ2w4RojeTA4fQAsWNhVThSWWlASJ7NE'
    notification_data = json.loads(str(request.form['data']))
    status = Notifications(temp_gcm_id).sendNotification(notification_data)
    return jsonify(status)

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

@webapp.route('/deleteRental', methods=['POST'])
def deleteRentals():
    lenders = [int(_) for _ in request.form['order_id'].split(",")]
    for lender_id in lenders:
        Lend.deleteRental(lender_id)
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

@webapp.route('/crawl')
def crawlItem():
    amzn_url = Utils.getParam(request.args, 'url')
    book_data = getAggregatedBookDetails(amzn_url)
  
    final_data = Admin.insertItem(book_data)
    return jsonify(final_data) 

@webapp.route('/getContent')
def getContent():
    return jsonify(Search().getContentData())

@webapp.route('/getNewContent')
def getNewContent():
    all_content = []
    # NOTE make this generic in dashboard
    # hard coded panel ids for now
    for panel_id in [3,4,5]:
        all_content.append(Collection(panel_id).getExpandedObj())
    return jsonify(all_content)

@webapp.route('/saveContent')
def saveContent():
    Collection.saveCollectionData(request.args)
    #Admin.savePanelData(request.args)
    return jsonify(status=True)

@webapp.route('/getSearchFails')
def getSearchFails():
    return jsonify(data=Admin.getSearchFailedQueries())

@webapp.route('/searchFailItem')
def searchFailItem():
    Admin.submitSearchFailItem(request.args)
    return jsonify(status=True)

@webapp.route('/searchFailNotification')
def searchFailNotification():
    Admin.sendSearchFailNotification(request.args)
    return jsonify(status=True)

@webapp.route('/incrementInventory')
def incrementInventory():
    item_data = Admin.addItemToInventory(int(request.args.get('item_id')))
    return jsonify(item_data)

@webapp.route('/updateAreas', methods=['POST'])
def updateAreas():
    Admin.updateAreas(request.form)
    return jsonify(status='True')

@webapp.route('/orderComment')
def orderComment():
    comment_data = {}
    for key in request.args:
        comment_data[key] = request.args[key]
    comment_data['edited'] = 1
    Admin.updateOrderComment(comment_data)
    return jsonify(status=True)
