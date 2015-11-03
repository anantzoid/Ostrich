from app import webapp
from app.models import User, Helpers
from flask import request, jsonify

@webapp.route('/preregister', methods=['POST'])
def preregister():
    email = Helpers.getParam(request.form, 'email')
    if email:
        User.preregisterUser(email)
    return jsonify({'success': 'true'});

@webapp.route('/fetchUser', methods=['POST'])
def fetchUser():
    response = {'status': 'False'}

    social_id = Helpers.getParam(request.form, 'id') 
    if not social_id:
        response['message'] = 'Social ID missing'
        return jsonify(response)

    source = Helpers.getParam(request.form, 'source') 
    if not source:
        response['message'] = 'Login source missing'
        return jsonify(response)

    user = User(social_id, source) 
    return jsonify(user.getObj())

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
    user_id = Helpers.getParam(request.form, 'user_id')
    if not user_id:
        response['message'] = 'User ID missing'
        return jsonify(response)

    address = request.form['address']  if 'address' in request.form else ''
    if not address:
        response['message'] = 'Address missing'
        return jsonify(response)

    user = User(user_id, 'user_id')
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
    user_id = Helpers.getParam(request.form, 'user_id')
    if not user_id:
        return jsonify(response)
    
    user_data = {}
    for key in request.form:
        user_data[key] = request.form[key]

    user = User(user_id, 'user_id')
    status = user.editDetails(user_data)
    if status:
        response['status'] = 'True'
    return jsonify(response)


@webapp.route('/myOrders', methods=['POST'])
def getMyOrders():
    response = {'status': 'false'}
    user_id = Helpers.getParam(request.form, 'user_id')
    if not user_id:
        return jsonify(response)

    user = User(int(user_id), 'user_id')
    orders = user.getOrders()
    return jsonify(orders)


@webapp.route('/putReferral', methods=['POST'])
def putReferral():
    response = {'status': 'False'}
    user_id = Helpers.getParam(request.form, 'user_id')
    if not user_id:
        return jsonify(response)
    
    uuid = Helpers.getParam(request.form, 'uuid')
    if not uuid:
        return jsonify(response)

    user = User(int(user_id), 'user_id')
    referral_id = user.logReferral(uuid)
    if not referral_id:
        response['message'] = 'User already existed'
    else:
        response['status'] = 'True'
        response['referral_id'] = referral_id

    return jsonify(response)
    

@webapp.route('/confirmReferral', methods=['POST'])
def confirmReferral():
    response = {'status': 'false'}
    user_id = Helpers.getParam(request.form, 'user_id')
    if not user_id:
        return jsonify(response)
 
    uuid = Helpers.getParam(request.form, 'uuid')
    if not uuid:
        return jsonify(response)

    user = User(int(user_id), 'user_id')
    result = user.confirmReferral(uuid)
    if not result:
        response['message'] = 'Referral not valid'
    else:
        response['status'] = 'True'

    return jsonify(response)

    
'''
TODO: remove this
@webapp.route('/updateInviteLevel', methods=['POST'])
def updateUserInvite():
    response = {'status': 'false'}
    user_id = Helpers.getParam(request.form, 'user_id')
    if not user_id:
        return jsonify(response)

    user = User(int(user_id), 'user_id')
    response['status'] = user.upgradeInviteScheme()
    return jsonify(response)
'''

