from app import webapp
from app.models import Search, Order, User
from flask import jsonify, request

@webapp.route('/startSession')
def startSession():
    if 'android_id' in request.args:
        android_id = request.args.get('android_id')
        if android_id in []:
            return jsonify({'debug':'True', 'ip': '52.74.20.228'})

    data = {
        'recommendations': Search([]).mostRecommended(),
        'most_searched': Search([]).mostSearched(),
        'categories': Search.getSearchCategories(),
        'return_days': webapp.config['DEFAULT_RETURN_DAYS'],
        'reading_multiplier': 1.43,
        'time_slots': Order.getTimeSlotsForOrder(),
        'user_model': None
    }

    if 'user_id' in request.args:
        user_id = request.args.get('user_id')
        user = User(user_id)
        user.getOrderSlotsNew()
        data['user_model'] = user.getObj()
    return jsonify(data)
