from app import webapp
from app.models import Search, Order, User
from flask import jsonify, request

@webapp.route('/startSession')
def startSession():
    data = {
        'recommendations': Search([]).mostRecommended(),
        'most_searched': Search([]).mostSearched(),
        'categories': Search.getSearchCategories(),
        'return_days': webapp.config['DEFAULT_RETURN_DAYS'],
        'reading_multiplier': 1,
        'time_slots': Order.getTimeSlotsForOrder(),
        'user_model': None
    }

    if 'user_id' in request.args:
        user_id = request.args.get('user_id')
        data['user_model'] = User(user_id).getObj()
    return jsonify(data)
