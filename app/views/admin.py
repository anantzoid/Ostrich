from app import webapp
from app.models import Admin
#from flask import request, jsonify
from flask.ext.jsonpify import jsonify

@webapp.route('/currentOrders')
def getCurrentOrders():
    current_order = Admin.getCurrentOrders()
    return jsonify(orders=current_order)

@webapp.route('/fetchInventoryDetail/<int:inventory_id>')
def fetchItemDetail(inventory_id):
    inv_data = Admin.getItemDetail(inventory_id)
    return jsonify(inv_data)

@webapp.route('/setInventoryData', methods=['POST'])
def setInventoryData():
    Admin.setInventoryData(request.form)
    return jsonify(status=True)

@webapp.route('/currentRentals')
def getCurrentRentals():
    current_rentals = Admin.getCurrentRentals()
    return jsonify(orders=current_rentals)
