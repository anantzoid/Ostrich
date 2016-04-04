from app import webapp
from app.models import Search, Order, User, Collection
from flask import jsonify, request

@webapp.route('/startSession')
def startSession():
    if 'android_id' in request.args:
        android_id = request.args.get('android_id')
        if android_id in []:
            return jsonify({'debug':'True', 'ip': '52.74.20.228'})

    # VERSION SPECIFIC
    app_version = int(request.headers.get('App-Version')) if 'App-Version' in request.headers else 0

    reading_multiplier = webapp.config['NEW_READING_RATE'] if app_version >= 6030000 else webapp.config['NEW_READING_RATE'] - 0.01
    data = {
        'most_searched': Collection(4).getExpandedObj()['items'],
        'recommendations': Collection(5).getExpandedObj()['items'],
        'categories': Search.getSearchCategories(),
        'return_days': webapp.config['DEFAULT_RETURN_DAYS'],
        'reading_multiplier': reading_multiplier,
        'time_slots': Order.getTimeSlotsForOrder(),
        'user_model': None
    }

    if 'user_id' in request.args:
        user_id = request.args.get('user_id')
        if user_id and int(user_id) > -1:
            user = User(user_id)
            user.getOrderSlots()
            data['user_model'] = user.getObj()
            user.logMetadata(app_version)
    return jsonify(data)
