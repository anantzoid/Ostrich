from app import webapp
from app.models import User, Utils
from flask import request, jsonify

@webapp.route('/preregister', methods=['POST'])
def preregister():
    email = Utils.getParam(request.form, 'email')
    if email:
        User.preregisterUser(email)
    return jsonify({'success': 'true'});

'''
    @params
        user_id: The current user's id
        source: {user_id, google_id, facebook_id(not supported currently)} 
    @response
        on error:
        status,
        message
        on success:
        user_object
'''
@webapp.route('/fetchUser', methods=['POST'])
def fetchUser():
    response = {'status': 'False'}

    social_id = Utils.getParam(request.form, 'id') 
    if not social_id:
        response['message'] = 'Social ID missing'
        return Utils.errorResponse(response, webapp.config['HTTP_STATUS_CODE_DATA_MISSING'])

    source = Utils.getParam(request.form, 'source') 
    if not source:
        response['message'] = 'Login source missing'
        return Utils.errorResponse(response, webapp.config['HTTP_STATUS_CODE_DATA_MISSING'])

    user = User(social_id, source) 
    if user.getObj() is not None:
        return jsonify(user.getObj())
    else:
        return Utils.errorResponse(response)

'''
    User registration call
    @params
        optional:
        username
        password
        name
        phone
        email
        address: list of address objects (check below)
        google_id: user's google+ id on google signup
        gcm_id: google cloud messaging id for notifications
        
    @response
        status, user_id(optional)
'''
@webapp.route('/signup', methods=['POST'])
def userSignup():
    user_data = {}

    for key in request.form:
        user_data[key] = request.form[key]

    user = User.createUser(user_data)
    if 'user' in user:
        return jsonify(user)
    else:
        user['status'] = 'False'
        return Utils.errorResponse(user)

'''
    Add address for a user
    @params
        user_id: The current user's id
        address: {
                    'address': descriptive address,
                    'longitude',
                    'latitude',
                    'address_id': optional, while editing address
                    }
    @response
        status, address_id (on success)
'''
@webapp.route('/addAddress', methods=['POST'])
def addAddress():
    response = {'status': 'False'}

    user_id = Utils.getParam(request.form, 'user_id')
    if not user_id:
        response['message'] = 'User ID missing'
        return Utils.errorResponse(response, webapp.config['HTTP_STATUS_CODE_DATA_MISSING'])

    address = request.form['address']  if 'address' in request.form else ''
    if not address:
        response['message'] = 'Address missing'
        return Utils.errorResponse(response, webapp.config['HTTP_STATUS_CODE_DATA_MISSING'])

    user = User(user_id, 'user_id')
    if user.getObj() is None:
        return Utils.errorResponse(response)

    address_id = user.addAddress(address)
    if address_id:
        response = {
                'status': 'True',
                'address_id': address_id[0]
                }
        return jsonify(response)
    else:
        return Utils.errorResponse(response)
        
'''
    Edit details of a user
    @params
        user_id: The current user's id
        (optional):
        username, name, phone, email, 
        address(object) :  supports only 1 address right now
    @response
        status
'''
@webapp.route('/editDetails', methods=['POST'])
def editDetails():
    response = {'status': 'False'}

    user_id = Utils.getParam(request.form, 'user_id', 'int')
    if not user_id:
        return Utils.errorResponse(response, webapp.config['HTTP_STATUS_CODE_DATA_MISSING'])
    
    user_data = {}
    for key in request.form:
        user_data[key] = request.form[key]

    user = User(user_id, 'user_id')
    if user.getObj() is None:
        return Utils.errorResponse(response)

    status = user.editDetails(user_data)
    if status:
        response['status'] = 'True'
        return jsonify(response)
    else:
        return Utils.errorResponse(response)


'''
    Gets a list of orders/rentals made by the users
    @params
        user_id: The current user's id
    @response
        status, List of order objects 
'''
@webapp.route('/myOrders', methods=['POST'])
def getMyOrders():
    response = {'status': 'false'}
    user_id = Utils.getParam(request.form, 'user_id')
    if not user_id:
        return Utils.errorResponse(response, webapp.config['HTTP_STATUS_CODE_DATA_MISSING'])

    user = User(int(user_id), 'user_id')
    if user.getObj() is None:
        return Utils.errorResponse(response)

    orders = user.getAllOrders()
    orders.update(user.getAllRentals())
    return jsonify(orders)

'''
    Log on inviting another user
    @params
        user_id: The current user's id
        uuid: Unique code provided by google invite api
    @response
        status, message(optional)
'''
@webapp.route('/putReferral', methods=['POST'])
def putReferral():
    response = {'status': 'False'}

    user_id = Utils.getParam(request.form, 'user_id')
    if not user_id:
        return Utils.errorResponse(response, webapp.config['HTTP_STATUS_CODE_DATA_MISSING'])
    
    uuid = Utils.getParam(request.form, 'uuid')
    if not uuid:
        return Utils.errorResponse(response, webapp.config['HTTP_STATUS_CODE_DATA_MISSING'])

    user = User(int(user_id), 'user_id')
    if user.getObj() is None:
        return Utils.errorResponse(response)

    referral_id = user.logReferral(uuid)
    if not referral_id:
        response['message'] = 'User already existed'
        return Utils.errorResponse(response, webapp.config['HTTP_STATUS_CODE_ENTRY_EXISTS'])
    else:
        response['status'] = 'True'
        response['referral_id'] = referral_id
        return jsonify(response)
    

'''
    Accept invitation from a user, by clicking on the referral link
    @params
        user_id: The current user's id 
        uuid: Unique code provided by google invite api
    @response
        status, message(optional)
'''
@webapp.route('/confirmReferral', methods=['POST'])
def confirmReferral():
    response = {'status': 'false'}

    user_id = Utils.getParam(request.form, 'user_id')
    if not user_id:
        return Utils.errorResponse(response, webapp.config['HTTP_STATUS_CODE_DATA_MISSING'])
 
    uuid = Utils.getParam(request.form, 'uuid')
    if not uuid:
        return Utils.errorResponse(response, webapp.config['HTTP_STATUS_CODE_DATA_MISSING'])

    user = User(int(user_id), 'user_id')
    if user.getObj() is None:
        return Utils.errorResponse(response)

    result = user.confirmReferral(uuid)
    if not result:
        response['message'] = 'Referral not valid'
        return Utils.errorResponse(response)
    else:
        response['status'] = 'True'
        response['message'] = 'Success! Check your wallet for free credits.'

        return jsonify(response)

'''
    Apply given referral code to ger credits
    @params
        user_id: The current user's id
        code: Referral code obtained from some other user
    @response
        status, message(optional)
'''
@webapp.route('/applyReferralCode', methods=['POST'])
def applyReferralCode():
    response = {'status': 'false'}

    user_id = Utils.getParam(request.form, 'user_id')
    if not user_id:
        return Utils.errorResponse(response, webapp.config['HTTP_STATUS_CODE_DATA_MISSING'])
 
    code = Utils.getParam(request.form, 'code')
    if not code:
        return Utils.errorResponse(response, webapp.config['HTTP_STATUS_CODE_DATA_MISSING'])
    
    user = User(int(user_id), 'user_id')
    if user.getObj() is None:
        return Utils.errorResponse(response)

    status = user.applyReferralCode(code)

    if not status:
        response['message'] = 'Code not applicable'
        return Utils.errorResponse(response)
    else:
        response['status'] = 'true'
        response['message'] = 'Code applied successfully'

        return jsonify(response)

#TODO uncomment this when authentication is made
'''
@webapp.route('/deleteUser')
def deleteUser():
    # TODO sessions stuff
    ids = request.args.get('id').split(',')
    User.deleteUser(ids)
    return jsonify(status=True)
'''
