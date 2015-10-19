from app import webapp
from app.models import User
from flask import request, jsonify

@webapp.route('/signup', methods=['POST'])
def userSignup():
    user_data = {}

    for key in request.form:
        user_data[key] = request.form[key]

    user_id = User.createUser(user_data)
    if 'user_id' in user_id:
        user_id['status'] = 'True'
    else:
        user_id['status'] = 'False'

    return jsonify(user_id)

@webapp.route('/addAddress', methods=['POST'])
def addAddress():
    response = {'status': 'False'}
    user_id = int(request.form['user_id']) if 'user_id' in request.form else ''
    if not user_id:
        response['message'] = 'User ID missing'
        return jsonify(response)

    address = request.form['address']  if 'address' in request.form else ''
    if not address:
        response['message'] = 'Address missing'
        return jsonify(response)

    user = User(user_id)
    address_id = user.addAddress(address)
    if address_id:
        response = {
                'status': 'True',
                'address_id': address_id
                }

    return jsonify(response)
        

@webapp.route('/editDetails', methods=['POST'])
def editDetails():
    response = {'status': 'False'}
    user_id = int(request.form['user_id']) if 'user_id' in request.form else ''
    if not user_id:
        response['message'] = 'User ID missing'
        return jsonify(response)
    
    user_data = {}
    for key in request.form:
        user_data[key] = request.form[key]

    user = User(user_id)
    status = user.editDetails(user_data)
    if status:
        response['status'] = 'True'

    return jsonify(response)

