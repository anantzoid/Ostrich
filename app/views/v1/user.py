from app import webapp
from app.models import User, Utils, Notifications
from flask import request, jsonify
import json

@webapp.route('/preregister', methods=['GET'])
def preregister():
    response = {'status': 'False'}

    user_data = {}
    user_data['email'] = Utils.getParam(request.args, 'email')
    user_data['phone'] = Utils.getParam(request.args, 'phone')
    user_data['book_id'] = Utils.getParam(request.args, 'bookid', 'int')
    user_data['org'] = Utils.getParam(request.args, 'org')

    for key in user_data.keys():
        if not key:
            Utils.errorResponse(response)
    
    User.b2bUser(user_data)
    return jsonify({'status': 'True'});

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
        return Utils.errorResponse(response)

    source = Utils.getParam(request.form, 'source') 
    if not source:
        response['message'] = 'Login source missing'
        return Utils.errorResponse(response)

    user = User(social_id, source) 
    if user.getObj() is not None:
        user.getOrderSlots()
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
    user_data['app_version'] = int(request.headers.get('App-Version')) if 'App-Version' in request.headers else 0

    user = User.createUser(user_data)
    if 'user_id' in user:
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
        return Utils.errorResponse(response, 'HTTP_STATUS_CODE_DATA_MISSING')

    address = request.form['address']  if 'address' in request.form else ''
    if not address:
        response['message'] = 'Address missing'
        return Utils.errorResponse(response, 'HTTP_STATUS_CODE_DATA_MISSING')

    user = User(user_id, 'user_id')
    if user.getObj() is None:
        return Utils.errorResponse(response)

    address_id = user.addAddress(address)
    if address_id:
        user = User(user_id, 'user_id')
        user.getOrderSlots()
        address_obj = [_ for _ in user.address if _['address_id'] == address_id[0]][0]
        return jsonify(address_obj)
    else:
        return Utils.errorResponse(response)

@webapp.route('/validateLocality', methods=['POST'])
def validateLocality():
    response = {'status': 'False'}

    locality = Utils.getParam(request.form, 'locality', '')
    if not locality:
        return Utils.errorResponse(response, 'HTTP_STATUS_CODE_DATA_MISSING')

    response = User.validateLocality(locality)
    return jsonify(response)


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
        return Utils.errorResponse(response, 'HTTP_STATUS_CODE_DATA_MISSING')
    
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
        return Utils.errorResponse(response, 'HTTP_STATUS_CODE_DATA_MISSING')

    user = User(int(user_id), 'user_id')
    if user.getObj() is None:
        return Utils.errorResponse(response)

    orders = user.getAllOrders()
    orders.update(user.getAllRentals())
    return jsonify(orders)

@webapp.route('/getWishlist')
def getWishlist():
    response = {'status': 'False'}
    user_id = Utils.getParam(request.args, 'user_id', 'int')
    if user_id:
        return json.dumps(User.getWishlist(user_id))
    return Utils.errorResponse(response)

@webapp.route('/addToWishlist', methods=['POST'])
def addToWishlist():
    User.addToWishlist(request.form)
    return jsonify(status='True')

@webapp.route('/removeFromWishlist', methods=['POST'])
def removeFromWishlist():
    User.removeFromWishlist(request.form)
    return jsonify(status='True')

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
        return Utils.errorResponse(response, 'HTTP_STATUS_CODE_DATA_MISSING')
    
    uuid = Utils.getParam(request.form, 'uuid')
    if not uuid:
        return Utils.errorResponse(response, 'HTTP_STATUS_CODE_DATA_MISSING')

    user = User(int(user_id), 'user_id')
    if user.getObj() is None:
        return Utils.errorResponse(response)

    referral_id = user.logReferral(uuid)
    if not referral_id:
        response['message'] = 'User already existed'
        return Utils.errorResponse(response, 'HTTP_STATUS_CODE_ENTRY_EXISTS')
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
        return Utils.errorResponse(response, 'HTTP_STATUS_CODE_DATA_MISSING')
 
    uuid = Utils.getParam(request.form, 'uuid')
    if not uuid:
        return Utils.errorResponse(response, 'HTTP_STATUS_CODE_DATA_MISSING')

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
        return Utils.errorResponse(response, 'HTTP_STATUS_CODE_DATA_MISSING')
 
    code = Utils.getParam(request.form, 'code')
    if not code:
        return Utils.errorResponse(response, 'HTTP_STATUS_CODE_DATA_MISSING')
    
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
@webapp.route('/deleteUser2892967061')
def deleteUser():
    # TODO sessions stuff
    ids = request.args.get('id').split(',')
    User.deleteUser(ids)
    return jsonify(status=True)

@webapp.route('/sendMassNotification')
def sendMassNotification():
    notification_data = {}
    '''
    notification_data['notification_id'] = Utils.getParam(request.args, 'notification_id', var_type='int', default=10)
    notification_data['title'] = Utils.getParam(request.args, 'title')
    notification_data['message'] = Utils.getParam(request.args, 'message')
    notification_data['image_url'] = Utils.getParam(request.args, 'image_url')
    notification_data['post_url'] = Utils.getParam(request.args, 'post_url')
    notification_data['social_media'] = Utils.getParam(request.args, 'social_media')
    admin_flag = Utils.getParam(request.args, 'admin', var_type='int', default=0)
    '''

    for arg in request.args:
        notification_data[arg] = request.args[arg]
    if not 'notification_id' in notification_data:
        notification_data['notification_id'] = 10
    if 'admin' in notification_data:
        admin_flag = int(notification_data['admin'])
    for key in notification_data:
        if not notification_data[key]:
            Utils.errorResponse({'status': 'False'})
    Notifications().sendMassNotification(notification_data, admin_flag)
    return jsonify(status=True)
